from packages.agents.base import BaseAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class KeywordAgent(BaseAgent):
    definition = AgentDefinition(
        name="keyword_agent",
        label="Keyword Agent",
        purpose="Generate candidate player-need keywords for one game and topic.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        game = request.game_name
        keywords = [
            f"{game} {request.topic}",
            f"{game} black screen fix",
            f"{game} Steam Deck settings",
            f"{game} save file location",
            f"{game} controller not working",
        ]
        return AgentRunResponse(agent=self.definition.name, output={"keywords": keywords})

