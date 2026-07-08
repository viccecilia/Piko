from packages.improvement.regression_runner import default_regression_plan
from packages.shared.schemas import PatchPlan, PatchPlanStep, UpgradeProposal


def patch_plan_from_proposal(proposal: UpgradeProposal) -> PatchPlan:
    steps = [
        PatchPlanStep(
            step_id=f"step_{index:03d}",
            target_file=module,
            change_summary="Prepare a targeted code or test change for operator approval.",
            reason=proposal.reason,
            verification="Run the regression command plan after an operator-approved worker implements the change.",
        )
        for index, module in enumerate(proposal.affected_modules, start=1)
    ]
    return PatchPlan(
        plan_id=f"patch_plan_{proposal.proposal_id}",
        proposal_id=proposal.proposal_id,
        summary="Plan only; no patch is applied by the self-improvement loop.",
        steps=steps,
        regression_commands=default_regression_plan(),
        auto_apply_allowed=False,
    )

