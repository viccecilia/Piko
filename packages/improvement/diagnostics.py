from packages.shared.schemas import (
    DiagnosticReport,
    ImprovementPriority,
    ImprovementSignal,
    VerificationReport,
    VerificationStatus,
)


MODULE_BY_CHECK = {
    "source_evidence": "packages/agents/source_agent.py",
    "evidence_source_trace": "packages/indexing/evidence_extractor.py",
    "ranked_step_trace": "packages/agents/ranking_agent.py",
    "gate_decision_consistency": "packages/workflows/verification.py",
    "no_publishing_side_effect": "packages/workflows/article_pipeline.py",
}


def signals_from_verification_report(report: VerificationReport) -> list[ImprovementSignal]:
    signals: list[ImprovementSignal] = []
    for index, check in enumerate(report.checks, start=1):
        if check.status == VerificationStatus.passed:
            continue
        priority = ImprovementPriority.high if check.status == VerificationStatus.failed else ImprovementPriority.medium
        signals.append(
            ImprovementSignal(
                signal_id=f"signal_{index:03d}_{check.name}",
                priority=priority,
                failed_check=check.name if check.status == VerificationStatus.failed else None,
                warning=check.name if check.status == VerificationStatus.warning else None,
                risk="verification_failed" if check.status == VerificationStatus.failed else "verification_warning",
                suggested_fix=f"Investigate verification check '{check.name}': {check.message}",
                affected_module=MODULE_BY_CHECK.get(check.name, "packages/workflows/verification.py"),
                evidence=check.details,
            )
        )
    return signals


def diagnostic_from_verification_report(report: VerificationReport) -> DiagnosticReport:
    signals = signals_from_verification_report(report)
    return DiagnosticReport(
        diagnostic_id=f"diagnostic_{report.run_id or 'unknown'}",
        source_workflow=report.workflow,
        run_id=report.run_id,
        status="needs_improvement" if signals else "no_action",
        signals=signals,
        summary=f"{len(signals)} improvement signal(s) generated from verification status {report.status.value}.",
    )

