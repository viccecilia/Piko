from fastapi import APIRouter

from packages.shared.tool_registry import tool_registry


router = APIRouter()


@router.get("")
def list_tools() -> dict[str, object]:
    return {"tools": [tool.model_dump() for tool in tool_registry.list_tools()]}

