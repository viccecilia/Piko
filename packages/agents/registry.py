from packages.agents.base import BaseAgent
from packages.agents.conflict_agent import ConflictAgent
from packages.agents.editor_agent import EditorAgent
from packages.agents.evidence_agent import EvidenceAgent
from packages.agents.factcheck_agent import FactcheckAgent
from packages.agents.keyword_agent import KeywordAgent
from packages.agents.pain_agent import PainAgent
from packages.agents.ranking_agent import RankingAgent
from packages.agents.source_agent import SourceAgent
from packages.agents.writer_agent import WriterAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


BUSINESS_AGENT_NAMES = [
    "keyword_agent",
    "pain_agent",
    "source_agent",
    "evidence_agent",
    "conflict_agent",
    "ranking_agent",
    "writer_agent",
    "editor_agent",
]


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.definition.name] = agent

    def list_agents(self, include_quality_agents: bool = False) -> list[AgentDefinition]:
        names = self._agents.keys() if include_quality_agents else BUSINESS_AGENT_NAMES
        return [self._agents[name].definition for name in names if name in self._agents]

    def list_all_agents(self) -> list[AgentDefinition]:
        return [agent.definition for agent in self._agents.values()]

    def run(self, name: str, request: AgentRunRequest) -> AgentRunResponse:
        if name not in self._agents:
            available = ", ".join(sorted(self._agents))
            raise KeyError(f"Unknown agent '{name}'. Available agents: {available}")
        return self._agents[name].run(request)


agent_registry = AgentRegistry()
for _agent in [
    KeywordAgent(),
    PainAgent(),
    SourceAgent(),
    EvidenceAgent(),
    ConflictAgent(),
    RankingAgent(),
    WriterAgent(),
    EditorAgent(),
    FactcheckAgent(),
]:
    agent_registry.register(_agent)

