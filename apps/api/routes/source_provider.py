from fastapi import APIRouter, Response

from packages.source_provider.pipeline import operator_surface_artifact, operator_surface_html


router = APIRouter()


@router.get("/result")
def source_provider_result() -> dict[str, object]:
    return operator_surface_artifact()


@router.get("/window")
def source_provider_window() -> Response:
    return Response(content=operator_surface_html(), media_type="text/html")
