from fastapi import APIRouter, Response

from packages.external_endpoint.pipeline import (
    operator_external_endpoint_html,
    operator_external_endpoint_result,
)

router = APIRouter()


@router.get("/result")
def external_endpoint_result() -> dict[str, object]:
    return operator_external_endpoint_result()


@router.get("/window")
def external_endpoint_window() -> Response:
    return Response(content=operator_external_endpoint_html(), media_type="text/html")
