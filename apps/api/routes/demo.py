from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from packages.workflows.demo_run import run_operator_demo


router = APIRouter()


class DemoRunRequest(BaseModel):
    game_name: str = Field(default="Example Game", min_length=1)
    player_question: str = Field(default="crash on startup", min_length=1)
    mode: Literal["fixture", "real-source"] = "fixture"
    use_llm_writer: bool = False


@router.post("/run")
def run_demo(request: DemoRunRequest) -> dict[str, object]:
    try:
        return run_operator_demo(
            game_name=request.game_name,
            player_question=request.player_question,
            mode=request.mode,
            use_llm_writer=request.use_llm_writer,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
