from abc import ABC, abstractmethod

from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class BaseAgent(ABC):
    definition: AgentDefinition

    @abstractmethod
    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        """Run the agent and return structured JSON output."""

