from fastapi import APIRouter, Response

from packages.v03_practical_plugin.pipeline import trace_window_html, v03_status


router = APIRouter()


@router.get("/status")
def status() -> dict:
    return v03_status()


@router.get("/trace-window")
def trace_window() -> Response:
    return Response(content=trace_window_html(), media_type="text/html")
