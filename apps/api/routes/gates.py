from fastapi import APIRouter

from packages.gates.registry import gate_registry
from packages.shared.schemas import ArticleBrief


router = APIRouter()


@router.get("")
def list_gates() -> dict[str, object]:
    return {"gates": gate_registry.list_gate_names()}


@router.post("/evaluate")
def evaluate_gates(article_brief: ArticleBrief) -> dict[str, object]:
    results = gate_registry.evaluate_all(article_brief)
    return {"results": [result.model_dump() for result in results]}

