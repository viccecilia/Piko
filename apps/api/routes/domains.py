from fastapi import APIRouter, Response

from packages.domain_plugins.pipeline import domain_operator_surface, domain_registry, domains_window_html, route_domain


router = APIRouter()


@router.get("")
def list_domains() -> dict:
    registry = domain_registry()
    return {
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": False,
        "active_domain": registry["active_domain"],
        "domains": registry["domains"],
    }


@router.get("/window")
def domains_window() -> Response:
    return Response(content=domains_window_html(), media_type="text/html")


@router.get("/{domain_id}")
def get_domain_route(domain_id: str) -> dict:
    return route_domain(domain_id)


@router.get("/operator/surface")
def get_domain_operator_surface() -> dict:
    return domain_operator_surface()
