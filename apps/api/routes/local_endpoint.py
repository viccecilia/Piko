from fastapi import APIRouter, Response

from packages.local_endpoint.pipeline import (
    local_endpoint_payload,
    operator_endpoint_result_artifact,
    operator_endpoint_result_html,
)

router = APIRouter()


@router.get("/approved-json")
def approved_json_endpoint() -> dict[str, object]:
    return local_endpoint_payload()


@router.get("/result")
def endpoint_result() -> dict[str, object]:
    return operator_endpoint_result_artifact()


@router.get("/window")
def endpoint_window() -> Response:
    return Response(content=operator_endpoint_result_html(), media_type="text/html")
