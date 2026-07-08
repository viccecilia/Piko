from packages.gates.base import BaseGate
from packages.gates.conflict_gate import ConflictGate
from packages.gates.evidence_gate import EvidenceGate
from packages.gates.factcheck_gate import FactcheckGate
from packages.gates.intent_gate import IntentGate
from packages.gates.original_value_gate import OriginalValueGate
from packages.gates.publish_gate import PublishGate
from packages.gates.readability_gate import ReadabilityGate
from packages.gates.risk_gate import RiskGate
from packages.shared.schemas import ArticleBrief, GateResult


class GateRegistry:
    def __init__(self) -> None:
        self._gates: list[BaseGate] = [
            IntentGate(),
            EvidenceGate(),
            ConflictGate(),
            RiskGate(),
            OriginalValueGate(),
            ReadabilityGate(),
            FactcheckGate(),
            PublishGate(),
        ]

    def list_gate_names(self) -> list[str]:
        return [gate.name for gate in self._gates]

    def evaluate_all(self, brief: ArticleBrief) -> list[GateResult]:
        return [gate.evaluate(brief) for gate in self._gates]


gate_registry = GateRegistry()

