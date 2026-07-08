import argparse
import json
import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from packages.shared.config import get_settings
from packages.shared.schemas import WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline


VALID_DEMO_MODES = {"fixture", "real-source"}


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "demo"


@contextmanager
def _temporary_env(overrides: dict[str, str]) -> Iterator[None]:
    previous = {key: os.environ.get(key) for key in overrides}
    try:
        for key, value in overrides.items():
            os.environ[key] = value
        get_settings.cache_clear()
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        get_settings.cache_clear()


def _demo_env_overrides(mode: str, use_llm_writer: bool) -> dict[str, str]:
    settings = get_settings()
    if mode not in VALID_DEMO_MODES:
        raise ValueError(f"Unsupported demo mode '{mode}'. Use fixture or real-source.")
    if mode == "real-source" and not settings.enable_real_connectors:
        raise ValueError("real-source demo mode requires PIKO_ENABLE_REAL_CONNECTORS=true.")

    overrides: dict[str, str] = {}
    if mode == "fixture":
        overrides["PIKO_ENABLE_REAL_CONNECTORS"] = "false"
        overrides["PIKO_LIVE_CONNECTOR_TEST"] = "false"
    else:
        overrides["PIKO_ENABLE_REAL_CONNECTORS"] = "true"
        overrides["PIKO_LIVE_CONNECTOR_TEST"] = "true"

    if use_llm_writer and settings.enable_llm_writer:
        overrides["PIKO_ENABLE_LLM_WRITER"] = "true"
    else:
        overrides["PIKO_ENABLE_LLM_WRITER"] = "false"
    return overrides


def run_operator_demo(
    *,
    game_name: str,
    player_question: str,
    mode: str = "fixture",
    use_llm_writer: bool = False,
    output_dir: str = "artifacts/demo_runs",
) -> dict[str, Any]:
    mode = mode or "fixture"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _slugify(f"{game_name}-{player_question}")
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / f"{timestamp}_{slug}.json"
    md_path = target / f"{timestamp}_{slug}.md"

    with _temporary_env(_demo_env_overrides(mode, use_llm_writer)):
        report = run_article_pipeline(
            WorkflowStartRequest(
                game_id=f"demo_{_slugify(game_name)}",
                game_name=game_name,
                topic=player_question,
            )
        )

    draft = report.pipeline_state.draft.body if report.pipeline_state.draft else ""
    source_agent_output = report.agent_outputs.get("source_agent", {})
    writer_output = report.agent_outputs.get("writer_agent", {})
    publish_decision = report.publish_decision.model_dump(mode="json") if report.publish_decision else None
    verification_report = report.verification_report.model_dump(mode="json") if report.verification_report else None

    artifact = {
        "game_name": game_name,
        "player_question": player_question,
        "mode": mode,
        "draft": draft,
        "sources": [source.model_dump(mode="json") for source in report.pipeline_state.sources],
        "evidence_cards": [card.model_dump(mode="json") for card in report.pipeline_state.evidence_cards],
        "ranked_steps": [step.model_dump(mode="json") for step in report.pipeline_state.ranked_steps],
        "agent_trace": [
            {
                "agent": record.agent,
                "status": record.status.value,
                "output_keys": sorted(record.output.keys()),
                "duration_ms": record.duration_ms,
            }
            for record in report.pipeline_state.agent_runs
        ],
        "verification_report": verification_report,
        "publish_action": report.publish_action,
        "publish_decision": publish_decision,
        "publish_ready": False,
        "publishing_performed": bool(report.pipeline_state.draft and report.pipeline_state.draft.publishing_performed),
        "real_collection_performed": bool(source_agent_output.get("real_collection_performed")),
        "llm_used": bool(writer_output.get("llm_used")),
        "artifact_paths": {
            "json": str(json_path),
            "markdown": str(md_path),
        },
    }
    json_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(draft, encoding="utf-8")
    return artifact


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise argparse.ArgumentTypeError("Use true or false.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an internal Piko operator demo flow.")
    parser.add_argument("--game-name", default="Example Game")
    parser.add_argument("--question", default="crash on startup")
    parser.add_argument("--mode", choices=sorted(VALID_DEMO_MODES), default="fixture")
    parser.add_argument("--use-llm-writer", type=_parse_bool, default=False)
    parser.add_argument("--output-dir", default="artifacts/demo_runs")
    args = parser.parse_args()

    try:
        artifact = run_operator_demo(
            game_name=args.game_name,
            player_question=args.question,
            mode=args.mode,
            use_llm_writer=args.use_llm_writer,
            output_dir=args.output_dir,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(artifact, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
