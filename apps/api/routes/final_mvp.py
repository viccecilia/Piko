from fastapi import APIRouter, Response

from packages.final_mvp.pipeline import build_finish_gate_artifacts, operator_window_html


router = APIRouter()


@router.get("/result")
def final_mvp_result() -> dict[str, object]:
    return build_finish_gate_artifacts()


@router.get("/window")
def final_mvp_window() -> Response:
    build_finish_gate_artifacts()
    return Response(content=operator_window_html(), media_type="text/html")
