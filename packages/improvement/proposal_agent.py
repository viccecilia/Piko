from packages.shared.schemas import DiagnosticReport, UpgradeProposal, UpgradeRisk


def proposal_from_diagnostic(report: DiagnosticReport) -> UpgradeProposal:
    if not report.signals:
        return UpgradeProposal(
            proposal_id=f"proposal_{report.diagnostic_id}",
            diagnostic_id=report.diagnostic_id,
            title="No-op improvement proposal",
            reason="Verification passed without failed or warning checks.",
            affected_modules=[],
            expected_benefit="No code change recommended.",
            risk=UpgradeRisk.low,
            required_tests=["python -m pytest", "python -m packages.workflows.article_pipeline"],
        )

    affected_modules = sorted({signal.affected_module for signal in report.signals})
    has_high = any(signal.priority == "high" for signal in report.signals)
    return UpgradeProposal(
        proposal_id=f"proposal_{report.diagnostic_id}",
        diagnostic_id=report.diagnostic_id,
        title="Address verification-derived improvement signals",
        reason=report.summary,
        affected_modules=affected_modules,
        expected_benefit="Improve traceability, gate consistency, or source-backed workflow quality before future publishing eligibility.",
        risk=UpgradeRisk.medium if has_high else UpgradeRisk.low,
        required_tests=["python -m pytest", "python -m packages.workflows.article_pipeline"],
    )

