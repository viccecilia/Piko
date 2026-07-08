from fastapi.testclient import TestClient

from apps.api.main import app
from packages.agents.registry import agent_registry
from packages.gates.registry import gate_registry
from packages.shared.schemas import (
    AgentRunRecord,
    ArticleBrief,
    EvidenceCard,
    GameContext,
    GateRunRecord,
    PipelineState,
    PublishDecisionValue,
    RankedSolution,
    SourceReference,
    WorkflowRunReport,
    WorkflowStartRequest,
)
from packages.workflows.article_pipeline import aggregate_publish_decision, run_article_pipeline


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_agent_registry_lists_eight_business_agents() -> None:
    agents = agent_registry.list_agents()
    assert len(agents) == 8
    assert {agent.name for agent in agents} == {
        "keyword_agent",
        "pain_agent",
        "source_agent",
        "evidence_agent",
        "conflict_agent",
        "ranking_agent",
        "writer_agent",
        "editor_agent",
    }


def test_gates_accept_mock_article_brief() -> None:
    results = gate_registry.evaluate_all(ArticleBrief())
    assert len(results) == 8
    assert all(result.decision in {"pass", "fail"} for result in results)


def test_workflow_runs_start_to_end() -> None:
    result = run_article_pipeline(WorkflowStartRequest())
    assert result.status == "completed"
    assert result.steps[0] == "keyword_agent"
    assert result.steps[-1] == "article_brief"
    assert "editor_agent" in result.agent_outputs
    assert result.publish_action == "draft_review"
    assert result.pipeline_state.player_question == "crash on startup"
    assert result.pipeline_state.sources
    assert result.pipeline_state.evidence_cards
    assert result.pipeline_state.ranked_steps
    assert result.pipeline_state.draft is not None
    assert result.pipeline_state.gate_results


def test_verification_window_loads() -> None:
    response = client.get("/verification/window")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Piko Verification Window" in response.text
    assert "/workflow/article-pipeline/run" in response.text


def test_minimal_pipeline_state_serializes_to_json() -> None:
    state = PipelineState(
        player_question="black screen after launch",
        game=GameContext(game_id="game_mock_002", game_name="Mock Quest"),
        intent="Help players fix a black screen after launch.",
    )

    payload = state.model_dump(mode="json")
    restored = PipelineState.model_validate(payload)

    assert restored.player_question == "black screen after launch"
    assert restored.game.game_name == "Mock Quest"
    assert restored.sources == []
    assert restored.evidence_cards == []


def test_pipeline_state_contract_contains_core_path_fields() -> None:
    brief = ArticleBrief()
    gate_result = gate_registry.evaluate_all(brief)[0]
    state = PipelineState(
        player_question="crash on startup",
        game=GameContext(game_id="game_mock_001", game_name="Example Game"),
        intent="Help players solve crash on startup in Example Game.",
        sources=[
            SourceReference(
                source_id="source_mock_official",
                source_type="official_notes",
                title="Mock official note",
            )
        ],
        evidence_cards=[
            EvidenceCard(
                evidence_card_id="ev_mock_001",
                source_id="source_mock_official",
                claim_type="solution",
                claim="Verify game files",
                solution="Verify game files",
                confidence=82,
            )
        ],
        ranked_steps=[
            RankedSolution(
                rank=1,
                solution="Verify game files",
                confidence=82,
                risk_level="low",
                source_ids=["source_mock_official"],
            )
        ],
        article_brief=brief,
        agent_runs=[AgentRunRecord(agent="ranking_agent", output={"ranked_solutions": []})],
        gate_results=[GateRunRecord(gate=gate_result.gate, result=gate_result)],
        decision="draft_review",
    )

    json_payload = state.model_dump_json()
    restored = PipelineState.model_validate_json(json_payload)

    assert restored.sources[0].source_id == "source_mock_official"
    assert restored.evidence_cards[0].source_id == "source_mock_official"
    assert restored.ranked_steps[0].risk_level == "low"
    assert restored.gate_results[0].result.decision in {"pass", "fail"}


def test_workflow_run_report_round_trips_with_pipeline_state() -> None:
    result = run_article_pipeline(WorkflowStartRequest())
    serialized = result.model_dump_json()
    restored = WorkflowRunReport.model_validate_json(serialized)

    assert restored.pipeline_state.decision == "draft_review"
    assert restored.pipeline_state.player_question == "crash on startup"
    assert restored.pipeline_state.gate_results[0].result.gate == "intent_gate"


def test_agent_run_records_are_observable() -> None:
    result = run_article_pipeline(WorkflowStartRequest())
    records = result.pipeline_state.agent_runs

    assert len(records) == 8
    assert all(record.input_summary["player_question"] == "crash on startup" for record in records)
    assert all(record.output for record in records)
    assert all(record.status == "completed" for record in records)
    assert all(record.duration_ms is not None and record.duration_ms >= 0 for record in records)
    assert all(record.error is None for record in records)


def test_article_workflow_api_accepts_player_question() -> None:
    response = client.post(
        "/workflow/article/run",
        json={
            "game_id": "game_mock_001",
            "game_name": "Example Game",
            "player_question": "crash on startup",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["pipeline_state"]["player_question"] == "crash on startup"
    assert payload["publish_decision"]["value"] == "verified_candidate"


def test_article_workflow_api_rejects_missing_question() -> None:
    response = client.post(
        "/workflow/article/run",
        json={"game_id": "game_mock_001", "game_name": "Example Game"},
    )

    assert response.status_code == 422


def test_publish_decision_blocks_risky_or_uncited_content() -> None:
    risky_state = PipelineState(
        sources=[
            SourceReference(source_id="source_1"),
            SourceReference(source_id="source_2"),
            SourceReference(source_id="source_3"),
        ],
        ranked_steps=[
            RankedSolution(rank=1, solution="Replace executable", confidence=80, risk_level="high", source_ids=["source_1"])
        ],
        gate_results=[],
    )
    weak_state = PipelineState(
        sources=[SourceReference(source_id="source_1")],
        ranked_steps=[
            RankedSolution(rank=1, solution="Verify game files", confidence=80, risk_level="low", source_ids=["source_1"])
        ],
        gate_results=[],
    )

    assert aggregate_publish_decision(risky_state).value == PublishDecisionValue.do_not_publish
    assert aggregate_publish_decision(weak_state).value == PublishDecisionValue.needs_more_evidence
