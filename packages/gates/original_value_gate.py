from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class OriginalValueGate(BaseGate):
    name = "original_value_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        has_ranking = len(brief.ranked_solutions) >= 2
        has_avoid_list = bool(brief.do_not_recommend)
        passed = has_ranking and has_avoid_list
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=84 if passed else 58,
            reasons=[
                "Brief includes ranked solutions.",
                "Brief includes what not to try first.",
            ] if passed else ["Brief needs ranking and risk-aware avoid-list value."],
            blocks_publish=not passed,
        )

