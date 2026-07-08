import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.capability_map.pipeline import ARTIFACT_DIR, capability_surface, run_batch


client = TestClient(app)


def test_capability_map_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "current_inventory.json",
        "skill_connector_inventory.json",
        "latest_capability_map.json",
        "capability_scorecard.json",
        "replacement_policy.json",
        "capability_registry.json",
        "routing_policy.json",
        "autonomy_levels.json",
        "human_approval_contract.json",
        "continuous_update_loop.json",
        "latest_cap_review_report.json",
    ]
    for name in required:
        payload = json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))
        assert payload


def test_capability_governance_guardrails_are_candidate_only() -> None:
    run_batch()
    review = json.loads((ARTIFACT_DIR / "latest_cap_review_report.json").read_text(encoding="utf-8"))
    replacement = json.loads((ARTIFACT_DIR / "replacement_policy.json").read_text(encoding="utf-8"))
    autonomy = json.loads((ARTIFACT_DIR / "autonomy_levels.json").read_text(encoding="utf-8"))

    assert review["guardrails"]["auto_install_performed"] is False
    assert review["guardrails"]["auto_replace_performed"] is False
    assert review["guardrails"]["publish_performed"] is False
    assert review["guardrails"]["deploy_performed"] is False
    assert replacement["runtime_replacement_performed"] is False
    assert autonomy["full_autonomous_publish_deploy_enabled"] is False


def test_capability_api_window_and_cli_surface_are_read_only() -> None:
    run_batch()
    cli = subprocess.run(
        [sys.executable, "-m", "packages.capability_map.pipeline", "--surface"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(cli.stdout)
    api = client.get("/capabilities")
    window = client.get("/capabilities/window")

    assert payload["candidate_only"] is True
    assert payload["runtime_changes_performed"] is False
    assert api.status_code == 200
    assert api.json()["publishing_performed"] is False
    assert window.status_code == 200
    assert "No auto-install" in window.text
    assert "human final approval" in window.text.lower()


def test_capability_surface_includes_routing_and_human_approval() -> None:
    run_batch()
    surface = capability_surface()
    route_types = {route["task_type"] for route in surface["routing_policy"]["routes"]}

    assert "source_collection" in route_types
    assert "verification" in route_types
    assert surface["human_approval_required_for_high_risk"] is True
