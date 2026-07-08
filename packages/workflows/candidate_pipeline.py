import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from packages.shared.schemas import (
    ArticleWorkflowRequest,
    DiscoveryArticleCandidate,
    PublishDecision,
    VerificationReport,
    PublishDecisionValue,
    WorkflowRunResult,
)
from packages.workflows.article_pipeline import run_article_workflow


class CandidateWorkflowResult(BaseModel):
    candidate_id: str
    workflow_request: ArticleWorkflowRequest
    workflow_result: WorkflowRunResult
    verification_report: VerificationReport | None = None
    publish_action: str
    publish_decision: PublishDecision | None = None
    publish_ready: bool = False
    publishing_performed: bool = False
    real_collection_performed: bool = False
    candidate_only: bool = True
    safety_fields: dict[str, Any] = Field(default_factory=dict)


def candidate_to_article_workflow_request(candidate: DiscoveryArticleCandidate) -> ArticleWorkflowRequest:
    return ArticleWorkflowRequest(
        game_id=candidate.game_id,
        game_name=candidate.game_name,
        player_question=candidate.player_question,
        article_intent=candidate.article_intent,
        candidate_id=candidate.candidate_id,
        cluster_id=candidate.cluster_id,
        source_query_hints=candidate.source_query_hints,
        safety_metadata={
            "decision": candidate.decision.value,
            "answer_status": candidate.answer_status.value,
            "risk_level": candidate.risk_level,
            "candidate_type": candidate.candidate_type,
            "runnable": candidate.runnable,
            "risk_flags": candidate.risk_flags,
            "safety_flags": candidate.safety_flags,
            "safety_reasons": candidate.safety_reasons,
            "safety_notes": candidate.safety_notes,
            "requires_evidence_pipeline": candidate.requires_evidence_pipeline,
            "candidate_only": True,
        },
        publish_ready=False,
        publishing_performed=False,
        real_collection_performed=False,
    )


def run_candidate_article_workflow(candidate: DiscoveryArticleCandidate) -> CandidateWorkflowResult:
    request = candidate_to_article_workflow_request(candidate)
    report = run_article_workflow(request)
    publishing_performed = bool(report.pipeline_state.draft and report.pipeline_state.draft.publishing_performed)
    real_collection_performed = any(
        bool(record.output.get("real_collection_performed"))
        for record in report.pipeline_state.agent_runs
    )
    publish_decision = report.publish_decision
    if report.verification_report and report.verification_report.status != "pass":
        publish_decision = PublishDecision(
            value=PublishDecisionValue.verification_failed,
            recommended_next_action="Keep candidate output blocked until verification passes.",
            reasons=[report.verification_report.summary],
            blocks_publish=True,
        )
    safety_fields = {
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": publishing_performed,
        "real_collection_performed": real_collection_performed,
        "requires_evidence_pipeline": candidate.requires_evidence_pipeline,
        "runnable_candidate": candidate.runnable,
        "risk_level": candidate.risk_level,
        "safety_flags": candidate.safety_flags,
        "verification_status": report.verification_report.status.value if report.verification_report else "missing",
        "publish_decision_blocks_publish": bool(publish_decision and publish_decision.blocks_publish),
        "discovery_is_publish_permission": False,
    }
    return CandidateWorkflowResult(
        candidate_id=candidate.candidate_id,
        workflow_request=request,
        workflow_result=report,
        verification_report=report.verification_report,
        publish_action=report.publish_action,
        publish_decision=publish_decision,
        publish_ready=False,
        publishing_performed=publishing_performed,
        real_collection_performed=real_collection_performed,
        candidate_only=True,
        safety_fields=safety_fields,
    )


def _candidate_slug(candidate: DiscoveryArticleCandidate) -> str:
    raw = f"{candidate.game_name}-{candidate.need_key}-{candidate.candidate_id}".lower()
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return slug or candidate.candidate_id


def _agent_trace(result: CandidateWorkflowResult) -> list[dict[str, Any]]:
    trace = []
    for record in result.workflow_result.pipeline_state.agent_runs:
        trace.append(
            {
                "agent": record.agent,
                "version": record.version,
                "status": record.status.value if hasattr(record.status, "value") else record.status,
                "input_summary": record.input_summary,
                "output_keys": sorted(record.output.keys()),
                "source_ids": record.output.get("source_ids", []),
                "error": record.error,
            }
        )
    return trace


def candidate_artifact_payload(
    candidate: DiscoveryArticleCandidate,
    result: CandidateWorkflowResult,
) -> dict[str, Any]:
    state = result.workflow_result.pipeline_state
    draft = state.draft.model_dump(mode="json") if state.draft else None
    payload = {
        "artifact_type": "discovery_candidate_draft",
        "status": "internal_draft_only",
        "candidate": candidate.model_dump(mode="json"),
        "workflow_request": result.workflow_request.model_dump(mode="json"),
        "workflow_result": result.workflow_result.model_dump(mode="json"),
        "draft": draft,
        "sources": [source.model_dump(mode="json") for source in state.sources],
        "evidence_cards": [card.model_dump(mode="json") for card in state.evidence_cards],
        "ranked_steps": [step.model_dump(mode="json") for step in state.ranked_steps],
        "agent_trace": _agent_trace(result),
        "verification_report": result.verification_report.model_dump(mode="json") if result.verification_report else None,
        "publish_decision": result.publish_decision.model_dump(mode="json") if result.publish_decision else None,
        "publish_action": result.publish_action,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": result.real_collection_performed,
        "candidate_only": True,
        "safety_fields": {
            **result.safety_fields,
            "artifact_internal_draft_only": True,
            "not_public_web_page": True,
            "long_raw_source_retained": False,
        },
    }
    return payload


def render_candidate_markdown_artifact(payload: dict[str, Any]) -> str:
    candidate = payload["candidate"]
    draft = payload.get("draft") or {}
    verification = payload.get("verification_report") or {}
    publish_decision = payload.get("publish_decision") or {}
    evidence_cards = payload.get("evidence_cards") or []
    sources = payload.get("sources") or []
    lines = [
        f"# Internal Draft: {candidate['game_name']} - {candidate['need_key']}",
        "",
        "**Status:** INTERNAL DRAFT - NOT PUBLISHED",
        "",
        "## Safety Status",
        f"- publish_ready: {payload['publish_ready']}",
        f"- publishing_performed: {payload['publishing_performed']}",
        f"- real_collection_performed: {payload['real_collection_performed']}",
        f"- candidate_only: {payload['candidate_only']}",
        f"- publish_decision: {publish_decision.get('value', 'missing')}",
        f"- verification_status: {verification.get('status', 'missing')}",
        "",
        "## Candidate",
        f"- Game: {candidate['game_name']}",
        f"- Question: {candidate['player_question']}",
        f"- Intent: {candidate['article_intent']}",
        f"- Decision: {candidate['decision']}",
        f"- Risk: {candidate['risk_level']}",
        "",
        "## Draft",
        draft.get("body") or "No draft body was produced.",
        "",
        "## Evidence Summary",
    ]
    if evidence_cards:
        for card in evidence_cards[:10]:
            lines.append(f"- {card.get('evidence_card_id')}: {card.get('claim') or card.get('solution') or card.get('symptom')}")
    else:
        lines.append("- No evidence cards were produced.")
    lines.extend(["", "## Sources"])
    if sources:
        for source in sources[:10]:
            lines.append(f"- {source.get('source_id')} ({source.get('source_type')}): {source.get('title') or source.get('url')}")
    else:
        lines.append("- No sources were produced.")
    lines.extend(
        [
            "",
            "## Next Action",
            publish_decision.get("recommended_next_action")
            or "Keep this candidate blocked until verification passes.",
            "",
        ]
    )
    return "\n".join(lines)


def write_candidate_workflow_artifacts(
    candidate: DiscoveryArticleCandidate,
    result: CandidateWorkflowResult,
    directory: str = "artifacts/candidate_drafts",
) -> tuple[Path, Path]:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    slug = _candidate_slug(candidate)
    json_path = target / f"{slug}.json"
    md_path = target / f"{slug}.md"
    payload = candidate_artifact_payload(candidate, result)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_candidate_markdown_artifact(payload), encoding="utf-8")
    return json_path, md_path
