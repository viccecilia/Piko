from fastapi import APIRouter

from packages.improvement.diagnostics import diagnostic_from_verification_report
from packages.improvement.patch_plan import patch_plan_from_proposal
from packages.improvement.proposal_agent import proposal_from_diagnostic
from packages.improvement.workflow_integration import (
    generate_improvement_report_from_verification,
    generate_improvement_report_from_workflow,
)
from packages.shared.schemas import DiagnosticReport, VerificationReport, WorkflowRunReport


router = APIRouter()


@router.post("/diagnose")
def diagnose(report: dict[str, object]) -> dict[str, object]:
    parsed = VerificationReport.model_validate(report)
    return diagnostic_from_verification_report(parsed).model_dump()


@router.post("/propose")
def propose(report: dict[str, object]) -> dict[str, object]:
    diagnostic = DiagnosticReport.model_validate(report)
    proposal = proposal_from_diagnostic(diagnostic)
    patch_plan = patch_plan_from_proposal(proposal)
    return {
        "upgrade_proposal": proposal.model_dump(),
        "patch_plan": patch_plan.model_dump(),
        "auto_apply_performed": False,
        "regression_executed": False,
    }


@router.post("/from-verification-report")
def from_verification_report(report: dict[str, object]) -> dict[str, object]:
    parsed = VerificationReport.model_validate(report)
    bundle = generate_improvement_report_from_verification(parsed)
    return {key: value.model_dump() if hasattr(value, "model_dump") else value for key, value in bundle.items()}


@router.post("/from-workflow-report")
def from_workflow_report(report: dict[str, object]) -> dict[str, object]:
    parsed = WorkflowRunReport.model_validate(report)
    bundle = generate_improvement_report_from_workflow(parsed)
    return {key: value.model_dump() if hasattr(value, "model_dump") else value for key, value in bundle.items()}
