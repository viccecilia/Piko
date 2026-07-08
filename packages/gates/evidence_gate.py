from packages.gates.base import BaseGate
from packages.shared.schemas import ArticleBrief, GateDecision, GateResult


class EvidenceGate(BaseGate):
    name = "evidence_gate"

    def evaluate(self, brief: ArticleBrief) -> GateResult:
        source_ids = {source_id for solution in brief.ranked_solutions for source_id in solution.source_ids}
        every_solution_cited = all(solution.source_ids for solution in brief.ranked_solutions)
        passed = every_solution_cited and len(source_ids) >= 3
        return GateResult(
            gate=self.name,
            decision=GateDecision.passed if passed else GateDecision.failed,
            score=86 if passed else 55,
            reasons=[
                f"Found {len(source_ids)} unique mock source IDs.",
                "Every ranked solution has source IDs." if every_solution_cited else "A ranked solution is missing source IDs.",
            ],
            blocks_publish=not passed,
        )

