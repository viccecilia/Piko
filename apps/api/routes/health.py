from fastapi import APIRouter

from packages.agents.registry import agent_registry
from packages.shared.config import get_settings


router = APIRouter()


@router.get("/health")
def health() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "stage": settings.stage,
        "registered_agents": len(agent_registry.list_agents()),
        "external_api_required": False,
        "publishing_enabled": False,
    }

