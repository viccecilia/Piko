from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class PublishGate(BaseGate):
    name = "publish_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        if brief.confidence >= 85:
            score = 85
            reason = "Eligible candidate for a future publishing round, but the current skeleton does not publish."
        elif brief.confidence >= 70:
            score = 75
            reason = "Suitable for draft review."
        elif brief.confidence >= 50:
            score = 55
            reason = "Store only until more evidence exists."
        else:
            score = 30
            reason = "Discard or wait for better evidence."
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if brief.confidence >= 70 else GateDecision.failed,
            score=score,
            reasons=[reason],
            blocks_publish=brief.confidence < 70,
        )
