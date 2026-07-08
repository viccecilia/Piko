import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.growth_loop.pipeline import ARTIFACT_DIR, run_batch


client = TestClient(app)


def test_growth_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "latest_scan_intake.json",
        "latest_normalized_candidates.json",
        "cap_review_policy.json",
        "latest_cap_review_report.json",
        "latest_capability_feedback.json",
        "worker_task_draft_contract.json",
        "verify_task_draft_contract.json",
        "latest_draft_queue_package.json",
        "latest_growth_review_report.json",
    ]
    for name in required:
        payload = json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))
        assert payload


def test_growth_cap_review_and_drafts_remain_safe() -> None:
    run_batch()
    review = json.loads((ARTIFACT_DIR / "latest_cap_review_report.json").read_text(encoding="utf-8"))
    queue = json.loads((ARTIFACT_DIR / "latest_draft_queue_package.json").read_text(encoding="utf-8"))
    feedback = json.loads((ARTIFACT_DIR / "latest_capability_feedback.json").read_text(encoding="utf-8"))

    assert review["active_capability_updated"] is False
    assert review["auto_apply_performed"] is False
    assert queue["status"] == "draft_only"
    assert queue["round_queue_files_created"] is False
    assert queue["auto_execute_performed"] is False
    assert queue["auto_apply_performed"] is False
    assert queue["runtime_adoption_performed"] is False
    assert queue["publish_ready"] is False
    assert queue["publishing_performed"] is False
    assert queue["network_performed"] is False
    assert queue["llm_performed"] is False
    assert feedback["active_capability_map_mutated"] is False
    for draft in queue["worker_drafts"]:
        assert draft["status"] == "draft_only"
        assert draft["auto_execute"] is False
    story_only = [item for item in review["decisions"] if item["decision"] == "story_only"]
    assert all(item["next_action"] == "story_pipeline_only" for item in story_only)


def test_growth_api_window_and_cli_are_read_only() -> None:
    run_batch()
    cli = subprocess.run(
        [sys.executable, "-m", "packages.growth_loop.pipeline", "--status"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(cli.stdout)
    api = client.get("/growth/status")
    window = client.get("/growth/window")

    assert payload["candidate_only"] is True
    assert payload["auto_execute_performed"] is False
    assert payload["runtime_adoption_performed"] is False
    assert api.status_code == 200
    assert api.json()["publish_ready"] is False
    assert api.json()["auto_apply_performed"] is False
    assert window.status_code == 200
    assert "Daily Growth" in window.text
    assert "Proposal only" in window.text
    assert "https://" not in window.text


def test_growth_final_review_guardrails_are_false() -> None:
    run_batch()
    final = json.loads((ARTIFACT_DIR / "latest_growth_review_report.json").read_text(encoding="utf-8"))
    assert final["next_round"] == "V02-1-R01"
    for value in final["guardrails"].values():
        assert value is False
