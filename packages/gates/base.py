from abc import ABC, abstractmethod

from packages.shared.schemas import ArticleBrief, GateResult


class BaseGate(ABC):
    name: str

    @abstractmethod
    def evaluate(self, brief: ArticleBrief) -> GateResult:
        """Evaluate a mock article brief."""

