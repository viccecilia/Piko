from fastapi import APIRouter, Response

from packages.v02_runtime.pipeline import trace_window_html


router = APIRouter()


@router.get("/trace-window")
def operator_trace_window() -> Response:
    return Response(content=trace_window_html(), media_type="text/html")
