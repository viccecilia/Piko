from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


BANNED_FILLER = ["this article will explore", "delve into", "in today's gaming landscape"]


class ReadabilityGate(BaseGate):
    name = "readability_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        haystack = f"{brief.article_intent} {brief.problem_statement}".lower()
        banned = [phrase for phrase in BANNED_FILLER if phrase in haystack]
        passed = bool(brief.quick_answer) and bool(brief.primary_user_pain) and not banned
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=88 if passed else 52,
            reasons=["Player can see what to try first from the brief."] if passed else [f"Readability issue: {banned or 'quick answer/pain missing'}"],
            blocks_publish=not passed,
        )
