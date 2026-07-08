from fastapi import APIRouter, Response

from packages.realdata.pipeline import build_realdata_artifacts, operator_window_html


router = APIRouter()


@router.get("/result")
def realdata_result() -> dict[str, object]:
    return build_realdata_artifacts()


@router.get("/window")
def realdata_window() -> Response:
    build_realdata_artifacts()
    return Response(content=operator_window_html(), media_type="text/html")
