from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class IntentGate(BaseGate):
    name = "intent_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        mixed_terms = ["map", "build", "patch notes", "save location"]
        mixed = [term for term in mixed_terms if term in brief.article_intent.lower()]
        passed = len(mixed) <= 1
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=90 if passed else 45,
            reasons=["Article brief targets one player need."] if passed else [f"Intent appears mixed: {mixed}"],
            blocks_publish=not passed,
        )

