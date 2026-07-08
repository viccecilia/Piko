from packages.agents.base import BaseAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class PainAgent(BaseAgent):
    definition = AgentDefinition(
        name="pain_agent",
        label="Pain Agent",
        purpose="Identify the concrete player pain behind a candidate topic.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "pain_type": "blocking_launch_issue",
                "pain_score": 82,
                "blocking_level": "high",
                "search_value": "medium",
                "article_candidate": True,
                "reason": "The mock topic blocks play and can be answered with a ranked solution path.",
            },
        )

