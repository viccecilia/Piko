from fastapi import APIRouter, Response

from packages.v04_langgraph_backend.pipeline import status_window_html, v04_status


router = APIRouter()


@router.get("/status")
def status() -> dict:
    return v04_status()


@router.get("/backend-window")
def backend_window() -> Response:
    return Response(content=status_window_html(), media_type="text/html")
