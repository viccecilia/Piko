from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class ConflictGate(BaseGate):
    name = "conflict_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        platform_safe = bool(brief.platform)
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if platform_safe else GateDecision.failed,
            score=82 if platform_safe else 50,
            reasons=["Platform scope is present."] if platform_safe else ["Platform scope is missing."],
            blocks_publish=not platform_safe,
        )

