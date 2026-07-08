from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class FactcheckGate(BaseGate):
    name = "factcheck_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        missing = [
            solution.solution
            for solution in brief.ranked_solutions
            if not solution.source_ids or solution.confidence < 50
        ]
        passed = not missing
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=85 if passed else 48,
            reasons=["Mock claim trace is complete."] if passed else [f"Claims need stronger traceability: {missing}"],
            blocks_publish=not passed,
        )

