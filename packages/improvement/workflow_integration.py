from packages.improvement.diagnostics import diagnostic_from_verification_report
from packages.improvement.patch_plan import patch_plan_from_proposal
from packages.improvement.proposal_agent import proposal_from_diagnostic
from packages.improvement.upgrade_ledger import make_ledger_entry
from packages.shared.schemas import (
    DiagnosticReport,
    PatchPlan,
    UpgradeLedgerEntry,
    UpgradeProposal,
    VerificationReport,
    WorkflowRunReport,
)
from packages.workflows.verification import verify_workflow_report


def generate_improvement_report_from_verification(report: VerificationReport) -> dict[str, object]:
    diagnostic = diagnostic_from_verification_report(report)
    proposal = proposal_from_diagnostic(diagnostic)
    patch_plan = patch_plan_from_proposal(proposal)
    ledger_entry = make_ledger_entry(proposal, patch_plan)
    return {
        "diagnostic_report": diagnostic,
        "upgrade_proposal": proposal,
        "patch_plan": patch_plan,
        "regression_plan": patch_plan.regression_commands,
        "ledger_entry": ledger_entry,
        "auto_apply_performed": False,
        "regression_executed": False,
        "publishing_state_mutated": False,
    }


def generate_improvement_report_from_workflow(report: WorkflowRunReport) -> dict[str, object]:
    verification = report.verification_report or verify_workflow_report(report)
    return generate_improvement_report_from_verification(verification)


class ImprovementReportBundle(dict):
    diagnostic_report: DiagnosticReport
    upgrade_proposal: UpgradeProposal
    patch_plan: PatchPlan
    ledger_entry: UpgradeLedgerEntry

