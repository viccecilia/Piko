from fastapi import APIRouter, Response

from packages.connector_registry.pipeline import build_operator_surface, connectors_window_html, plan_collection, route_connector
from packages.live_connector_pilot.pipeline import operator_live_connector_surface, operator_live_connector_window_html

router = APIRouter()


@router.get("")
def connector_surface() -> dict[str, object]:
    return build_operator_surface()


@router.get("/window")
def connector_window() -> Response:
    return Response(content=connectors_window_html(), media_type="text/html")


@router.get("/route")
def connector_route(domain_id: str, source_type: str | None = None) -> dict[str, object]:
    return route_connector(domain_id, source_type)


@router.post("/plan")
def connector_plan(domain_id: str, target_need: str = "candidate_need") -> dict[str, object]:
    return plan_collection(domain_id, target_need)


@router.get("/live")
def live_connector_surface() -> dict[str, object]:
    return operator_live_connector_surface()


@router.get("/live-window")
def live_connector_window() -> Response:
    return Response(content=operator_live_connector_window_html(), media_type="text/html")
