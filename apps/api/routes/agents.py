from fastapi import APIRouter

from packages.agents.registry import agent_registry
from packages.shared.schemas import AgentRunRequest, AgentRunResponse


router = APIRouter()


@router.get("")
def list_agents() -> dict[str, object]:
    return {"agents": [agent.model_dump() for agent in agent_registry.list_agents()]}


@router.post("/{agent_name}/run")
def run_agent(agent_name: str, request: AgentRunRequest) -> AgentRunResponse:
    return agent_registry.run(agent_name, request)

