from datetime import datetime, timezone
from time import perf_counter

from packages.agents.registry import BUSINESS_AGENT_NAMES, agent_registry
from packages.gates.registry import gate_registry
from packages.shared.config import get_settings
from packages.shared.schemas import (
    AgentRunRecord,
    AgentRunRequest,
    ArticleBrief,
    ArticleWorkflowRequest,
    ConflictRecord,
    DraftArtifact,
    EvidenceCard,
    GameContext,
    GateRunRecord,
    PipelineState,
    PublishDecision,
    PublishDecisionValue,
    RankedSolution,
    RunStatus,
    SourceReference,
    RunMonitoringSummary,
    WorkflowRunResult,
    WorkflowStartRequest,
)
from packages.workflows.verification import make_report_with_verification


def _initial_state(request: WorkflowStartRequest) -> PipelineState:
    return PipelineState(
        player_question=request.topic,
        game=GameContext(game_id=request.game_id, game_name=request.game_name),
        intent=f"Help players solve {request.topic} in {request.game_name}.",
    )


def _coerce_state(state: PipelineState | dict) -> PipelineState:
    if isinstance(state, PipelineState):
        return state
    return PipelineState.model_validate(state)


def _record_source_outputs(state: PipelineState, output: dict) -> None:
    for source in output.get("sources", []):
        state.sources.append(
            SourceReference(
                source_id=source["source_id"],
                source_type=source.get("source_type", "mock"),
                title=source.get("title"),
                url=source.get("url"),
                retrieved_at=source.get("retrieved_at"),
                trust_tier=source.get("trust_tier", "mock"),
                snippet=source.get("snippet"),
                clean_text=source.get("clean_text"),
                metadata=source.get("metadata", {}),
            )
        )


def _record_evidence_outputs(state: PipelineState, output: dict) -> None:
    for card in output.get("evidence_cards", []):
        state.evidence_cards.append(
            EvidenceCard(
                evidence_card_id=card["evidence_card_id"],
                source_id=card["source_id"],
                claim_type=card["claim_type"],
                claim=card.get("claim") or card.get("solution") or card.get("symptom"),
                source_type=card.get("source_type"),
                url=card.get("url"),
                retrieved_at=card.get("retrieved_at"),
                symptom=card.get("symptom"),
                solution=card.get("solution"),
                platform=card.get("platform"),
                version=card.get("version"),
                confidence=card.get("confidence", 0),
                risk_note=card.get("risk_note"),
            )
        )


def _record_conflict_outputs(state: PipelineState, output: dict) -> None:
    for index, conflict in enumerate(output.get("conflicts", []), start=1):
        state.conflicts.append(
            ConflictRecord(
                conflict_id=f"conflict_mock_{index:03d}",
                description=str(conflict),
                severity="medium",
            )
        )


def _record_ranking_outputs(state: PipelineState, output: dict) -> None:
    state.ranked_steps = [RankedSolution(**solution) for solution in output.get("ranked_solutions", [])]


def _record_writer_outputs(state: PipelineState, output: dict) -> None:
    state.draft = DraftArtifact(
        format=output.get("draft_format", "markdown"),
        body=output.get("draft_excerpt", ""),
        used_raw_sources=output.get("used_raw_sources", False),
        publishing_performed=output.get("publishing_performed", False),
    )


def _record_agent_output(state: PipelineState, agent_name: str, output: dict) -> None:
    if agent_name == "source_agent":
        _record_source_outputs(state, output)
    elif agent_name == "evidence_agent":
        _record_evidence_outputs(state, output)
    elif agent_name == "conflict_agent":
        _record_conflict_outputs(state, output)
    elif agent_name == "ranking_agent":
        _record_ranking_outputs(state, output)
    elif agent_name == "writer_agent":
        _record_writer_outputs(state, output)


def _run_agent_node(state: PipelineState | dict, agent_name: str) -> PipelineState:
    state = _coerce_state(state)
    started_at = datetime.now(timezone.utc)
    started_perf = perf_counter()
    input_summary = {
        "game_id": state.game.game_id,
        "game_name": state.game.game_name,
        "player_question": state.player_question,
    }
    payload = {}
    if agent_name == "evidence_agent":
        source_records = [
            source.model_dump(mode="json")
            for source in state.sources
            if source.source_type in {"pcgamingwiki", "mediawiki"} and (source.snippet or source.clean_text)
        ]
        if source_records:
            payload["source_records"] = source_records
    elif agent_name == "ranking_agent" and state.evidence_cards:
        payload["evidence_cards"] = [card.model_dump(mode="json") for card in state.evidence_cards]
    elif agent_name == "writer_agent" and state.evidence_cards and state.ranked_steps:
        payload.update(
            {
                "sources": [source.model_dump(mode="json") for source in state.sources],
                "evidence_cards": [card.model_dump(mode="json") for card in state.evidence_cards],
                "ranked_steps": [step.model_dump(mode="json") for step in state.ranked_steps],
                "article_intent": state.intent or f"Help players answer: {state.player_question}",
                "risk_notes": [
                    "Back up saves before moving, deleting, editing, or replacing files.",
                    "Do not download unknown recovery tools, DLL files, or patches.",
                ],
                "uncertainty_notes": ["Keep the draft unpublished until verification confirms claim traceability."],
            }
        )
    try:
        response = agent_registry.run(
            agent_name,
            AgentRunRequest(
                game_id=state.game.game_id,
                game_name=state.game.game_name,
                topic=state.player_question,
                payload=payload,
            ),
        )
        ended_at = datetime.now(timezone.utc)
        duration_ms = int((perf_counter() - started_perf) * 1000)
        state.agent_runs.append(
            AgentRunRecord(
                agent=agent_name,
                input_summary=input_summary,
                output=response.output,
                status=RunStatus.completed,
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
            )
        )
        _record_agent_output(state, agent_name, response.output)
        state.steps.append(agent_name)
    except Exception as exc:
        ended_at = datetime.now(timezone.utc)
        duration_ms = int((perf_counter() - started_perf) * 1000)
        state.agent_runs.append(
            AgentRunRecord(
                agent=agent_name,
                input_summary=input_summary,
                output={},
                status=RunStatus.failed,
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
                error=str(exc),
            )
        )
        state.status = RunStatus.failed
        state.errors.append(f"{agent_name}: {exc}")
        raise
    return state


def _build_article_brief(state: PipelineState | dict) -> PipelineState:
    state = _coerce_state(state)
    has_candidate_only_evidence = bool(state.evidence_cards) and not any(card.solution for card in state.evidence_cards)
    ranked_solutions = state.ranked_steps
    if not ranked_solutions and not has_candidate_only_evidence:
        ranked_solutions = [
            RankedSolution(
                rank=1,
                solution="Verify game files",
                confidence=78,
                risk_level="low",
                source_ids=["source_mock_official", "source_mock_forum"],
            )
        ]
    state.article_brief = ArticleBrief(
        game_id=state.game.game_id,
        game_name=state.game.game_name,
        title=f"{state.game.game_name} {state.player_question.title()} Fix",
        article_intent=state.intent or f"Help players solve {state.player_question} in {state.game.game_name}.",
        problem_statement=f"{state.game.game_name} players need a low-risk path for {state.player_question}.",
        primary_user_pain=f"Players are searching for a clear fix for {state.player_question}.",
        quick_answer=["Need more evidence before recommending a specific fix."] if has_candidate_only_evidence else ArticleBrief().quick_answer,
        ranked_solutions=ranked_solutions,
        confidence=45 if has_candidate_only_evidence else 78,
        risk_notes=[
            "Try reversible fixes first.",
            "Do not download unknown DLL files or replace executables from unofficial sources.",
            "Do not delete saves without a backup.",
            "Real source candidates are not enough to recommend an answer until page-level evidence is extracted.",
        ],
        source_summary=[
            f"{source.source_id} ({source.source_type})"
            for source in state.sources
        ],
        unresolved_questions=["Need page-level evidence for the player question."] if has_candidate_only_evidence else ([] if len(state.evidence_cards) >= 2 else ["Need more evidence from at least two source types."]),
        evidence_gaps=["Real source candidates found, but no answer-level evidence was extracted."] if has_candidate_only_evidence else ([] if state.evidence_cards else ["No evidence cards were available for this brief."]),
    )
    state.steps.append("article_brief")
    return state


def _run_sequential_pipeline(request: WorkflowStartRequest) -> PipelineState:
    state = _initial_state(request)
    for agent_name in BUSINESS_AGENT_NAMES:
        state = _run_agent_node(state, agent_name)
    return _build_article_brief(state)


def _run_langgraph_if_available(request: WorkflowStartRequest) -> PipelineState:
    try:
        from langgraph.graph import END, START, StateGraph
    except Exception:
        return _run_sequential_pipeline(request)

    try:
        graph = StateGraph(PipelineState)

        for agent_name in BUSINESS_AGENT_NAMES:
            graph.add_node(agent_name, lambda state, name=agent_name: _run_agent_node(state, name))
        graph.add_node("article_brief", _build_article_brief)

        graph.add_edge(START, BUSINESS_AGENT_NAMES[0])
        for current_agent, next_agent in zip(BUSINESS_AGENT_NAMES, BUSINESS_AGENT_NAMES[1:]):
            graph.add_edge(current_agent, next_agent)
        graph.add_edge(BUSINESS_AGENT_NAMES[-1], "article_brief")
        graph.add_edge("article_brief", END)

        compiled = graph.compile()
        return _coerce_state(compiled.invoke(_initial_state(request)))
    except Exception:
        return _run_sequential_pipeline(request)


def _legacy_publish_action(brief: ArticleBrief) -> str:
    settings = get_settings()
    if brief.confidence >= 85 and settings.publishing_enabled:
        return "auto_publish_disabled"
    if brief.confidence >= 70:
        return "draft_review"
    if brief.confidence >= 50:
        return "store_only"
    return "discard"


def aggregate_publish_decision(state: PipelineState) -> PublishDecision:
    failed_gates = [
        record.result.gate
        for record in state.gate_results
        if record.result.decision == "fail" or record.result.blocks_publish
    ]
    high_risk_steps = [step.solution for step in state.ranked_steps if step.risk_level == "high"]
    unresolved_conflicts = [conflict.conflict_id for conflict in state.conflicts if not conflict.resolved]
    source_ids = {source.source_id for source in state.sources}

    if not state.ranked_steps:
        return PublishDecision(
            value=PublishDecisionValue.needs_more_evidence,
            recommended_next_action="Keep as source candidate research until answer-level evidence and ranked steps exist.",
            reasons=["No ranked solution steps were produced from the available evidence."],
            blocks_publish=True,
        )
    if failed_gates:
        return PublishDecision(
            value=PublishDecisionValue.verification_failed,
            recommended_next_action="Keep as draft and fix failed gates before publishing.",
            reasons=[f"Failed or blocking gates: {', '.join(failed_gates)}"],
            blocks_publish=True,
        )
    if high_risk_steps:
        return PublishDecision(
            value=PublishDecisionValue.do_not_publish,
            recommended_next_action="Remove or downgrade high-risk steps before review.",
            reasons=[f"High-risk ranked steps: {', '.join(high_risk_steps)}"],
            blocks_publish=True,
        )
    if unresolved_conflicts:
        return PublishDecision(
            value=PublishDecisionValue.verification_failed,
            recommended_next_action="Resolve evidence conflicts before publishing.",
            reasons=[f"Unresolved conflicts: {', '.join(unresolved_conflicts)}"],
            blocks_publish=True,
        )
    if len(source_ids) < 3:
        return PublishDecision(
            value=PublishDecisionValue.needs_more_evidence,
            recommended_next_action="Collect more source-backed evidence before review.",
            reasons=[f"Only {len(source_ids)} unique source IDs are present."],
            blocks_publish=True,
        )
    return PublishDecision(
        value=PublishDecisionValue.verified_candidate,
        recommended_next_action="Eligible for later publishing eligibility checks; the current skeleton still performs no publishing.",
        reasons=["All mock gates passed with sufficient low-risk source-backed steps."],
        blocks_publish=False,
    )


def run_article_pipeline(request: WorkflowStartRequest) -> WorkflowRunResult:
    try:
        state = _run_langgraph_if_available(request)
        if state.article_brief is None:
            state = _build_article_brief(state)
        brief = state.article_brief
        gate_results = gate_registry.evaluate_all(brief)
        state.gate_results = []
        for result in gate_results:
            started_perf = perf_counter()
            state.gate_results.append(
                GateRunRecord(
                    gate=result.gate,
                    input_summary={"topic_id": brief.topic_id, "confidence": brief.confidence},
                    result=result,
                    status=RunStatus.completed,
                    duration_ms=int((perf_counter() - started_perf) * 1000),
                )
            )
        state.status = RunStatus.completed
        state.decision = _legacy_publish_action(brief)
        state.publish_decision = aggregate_publish_decision(state)
        total_duration = sum(record.duration_ms or 0 for record in state.agent_runs) + sum(record.duration_ms or 0 for record in state.gate_results)
        warnings = sum(1 for gate in state.gate_results for reason in gate.result.reasons if "warning" in reason.lower())
        state_errors = len(state.errors)
        monitoring = RunMonitoringSummary(
            total_duration_ms=total_duration,
            status=RunStatus.completed,
            warning_count=warnings,
            error_count=state_errors,
            estimated_tokens=sum(len(str(record.output)) // 4 for record in state.agent_runs),
        )
        state.monitoring_summary = monitoring
        agent_outputs = {record.agent: record.output for record in state.agent_runs}
        report = WorkflowRunResult(
            workflow="article_pipeline_v1",
            status="completed",
            steps=state.steps,
            agent_outputs=agent_outputs,
            article_brief=brief,
            gate_results=gate_results,
            publish_action=state.decision,
            pipeline_state=state,
            publish_decision=state.publish_decision,
        )
        return WorkflowRunResult.model_validate(make_report_with_verification(report).model_dump())
    except Exception:
        raise


def run_article_workflow(request: ArticleWorkflowRequest) -> WorkflowRunResult:
    return run_article_pipeline(
        WorkflowStartRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.player_question,
        )
    )


if __name__ == "__main__":
    result = run_article_pipeline(WorkflowStartRequest())
    print(result.model_dump_json(indent=2))
