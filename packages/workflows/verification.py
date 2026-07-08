from copy import deepcopy

from packages.shared.schemas import (
    VerificationCheck,
    VerificationReport,
    VerificationStatus,
    WorkflowRunReport,
)


def _check(name: str, ok: bool, message: str, details: dict | None = None, warning: bool = False) -> VerificationCheck:
    if ok:
        status = VerificationStatus.passed
    elif warning:
        status = VerificationStatus.warning
    else:
        status = VerificationStatus.failed
    return VerificationCheck(name=name, status=status, message=message, details=details or {})


def verify_workflow_report(report: WorkflowRunReport) -> VerificationReport:
    state = report.pipeline_state
    source_ids = {source.source_id for source in state.sources}
    evidence_source_ids = {card.source_id for card in state.evidence_cards}
    ranked_source_ids = {source_id for step in state.ranked_steps for source_id in step.source_ids}
    high_risk_steps = [step.solution for step in state.ranked_steps if step.risk_level == "high"]
    unresolved_conflicts = [conflict.conflict_id for conflict in state.conflicts if not conflict.resolved]
    failed_gates = [gate.result.gate for gate in state.gate_results if gate.result.decision == "fail"]
    publishing_side_effect = bool(state.draft and state.draft.publishing_performed)

    checks = [
        _check("player_need", bool(state.player_question and state.game.game_id), "Player need and game are present."),
        _check("source_evidence", bool(source_ids), "At least one traceable source is present.", {"source_count": len(source_ids)}),
        _check(
            "evidence_source_trace",
            evidence_source_ids.issubset(source_ids) and bool(evidence_source_ids),
            "Evidence cards link to known source IDs.",
            {"missing_source_ids": sorted(evidence_source_ids - source_ids)},
        ),
        _check(
            "ranked_step_trace",
            ranked_source_ids.issubset(source_ids),
            "Ranked steps use known source IDs.",
            {"missing_source_ids": sorted(ranked_source_ids - source_ids)},
        ),
        _check(
            "conflicts_surfaced",
            not unresolved_conflicts,
            "Unresolved conflicts must be surfaced before publish decisions.",
            {"unresolved_conflicts": unresolved_conflicts},
        ),
        _check(
            "risk_notes",
            not high_risk_steps or bool(state.article_brief and state.article_brief.risk_notes),
            "Risk notes are visible for risky actions.",
            {"high_risk_steps": high_risk_steps},
            warning=True,
        ),
        _check("no_publishing_side_effect", not publishing_side_effect, "Workflow did not publish content."),
        _check(
            "gate_decision_consistency",
            not (failed_gates and report.publish_decision and not report.publish_decision.blocks_publish),
            "Publish-ready decisions cannot coexist with failed gates.",
            {"failed_gates": failed_gates},
        ),
    ]

    if any(check.status == VerificationStatus.failed for check in checks):
        status = VerificationStatus.failed
    elif any(check.status == VerificationStatus.warning for check in checks):
        status = VerificationStatus.warning
    else:
        status = VerificationStatus.passed

    return VerificationReport(
        status=status,
        checks=checks,
        summary=f"{status.value}: {sum(check.status == VerificationStatus.passed for check in checks)}/{len(checks)} checks passed.",
        workflow=report.workflow,
        run_id=state.run_id,
    )


def make_report_with_verification(report: WorkflowRunReport) -> WorkflowRunReport:
    cloned = WorkflowRunReport.model_validate(deepcopy(report.model_dump()))
    verification = verify_workflow_report(cloned)
    cloned.verification_report = verification
    cloned.pipeline_state.verification_report = verification
    return cloned

