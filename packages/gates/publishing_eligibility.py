from packages.shared.schemas import PublishingEligibility, VerificationStatus, WorkflowRunReport


def evaluate_publishing_eligibility(report: WorkflowRunReport) -> PublishingEligibility:
    reasons: list[str] = []
    if report.verification_report is None or report.verification_report.status != VerificationStatus.passed:
        reasons.append("Verification has not passed.")
    if any(gate.decision == "fail" or gate.blocks_publish for gate in report.gate_results):
        reasons.append("One or more gates failed or blocks publishing.")
    if report.publish_decision is None or report.publish_decision.blocks_publish:
        reasons.append("Publish decision blocks publishing.")
    if any(conflict.severity == "high" and not conflict.resolved for conflict in report.pipeline_state.conflicts):
        reasons.append("High-risk unresolved conflicts are present.")
    if len({source.source_id for source in report.pipeline_state.sources}) < 3:
        reasons.append("Evidence source count is below threshold.")

    eligible = not reasons
    return PublishingEligibility(
        eligible=eligible,
        state="eligible_candidate" if eligible else "not_eligible",
        reasons=reasons or ["Verified source-backed candidate. Deployment is still disabled."],
        deploy_performed=False,
    )

