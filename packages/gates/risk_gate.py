from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class RiskGate(BaseGate):
    name = "risk_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        high_risk = [solution.solution for solution in brief.ranked_solutions if solution.risk_level == "high"]
        passed = not high_risk
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=92 if passed else 35,
            reasons=["No high-risk solution is recommended first."] if passed else [f"High-risk solutions present: {high_risk}"],
            blocks_publish=not passed,
        )

