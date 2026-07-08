from packages.agents.base import BaseAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class ConflictAgent(BaseAgent):
    definition = AgentDefinition(
        name="conflict_agent",
        label="Conflict Agent",
        purpose="Detect platform, version, source-age, and risk conflicts.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        topic = request.topic.lower()
        conflicts = []
        if "windows" in topic and "proton" in topic:
            conflicts.append(
                {
                    "type": "platform_mismatch",
                    "message": "Proton fixes apply to Steam Deck/Linux, not Windows.",
                    "severity": "medium",
                }
            )
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "conflicts": conflicts,
                "warnings": [
                    "Steam Deck fixes should not be mixed into the Windows quick answer without a platform note."
                ],
                "requires_human_review": bool(conflicts),
            },
        )
