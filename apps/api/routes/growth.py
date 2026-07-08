from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from packages.growth_loop.pipeline import growth_status, growth_window_html


router = APIRouter()


@router.get("/status")
def status() -> dict[str, object]:
    return growth_status()


@router.get("/window", response_class=HTMLResponse)
def window() -> str:
    return growth_window_html()

