from fastapi import APIRouter, Response

from packages.v05_langgraph_install.pipeline import status_window_html, v05_status


router = APIRouter()


@router.get("/status")
def status() -> dict:
    return v05_status()


@router.get("/langgraph-window")
def langgraph_window() -> Response:
    return Response(content=status_window_html(), media_type="text/html")
