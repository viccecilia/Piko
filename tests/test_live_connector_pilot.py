import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.live_connector_pilot.pipeline import (
    ARTIFACT_DIR,
    BLOCKED_FOR_ENDPOINT,
    SELECTED_CONNECTOR_ID,
    build_live_connector_artifacts,
    endpoint_readiness,
    live_connector_approval,
    live_connector_selection,
)


client = TestClient(app)


def test_live_connector_selection_only_allows_approved_json_endpoint() -> None:
    selection = live_connector_selection()
    approval = live_connector_approval()
    assert selection["selected_connector_id"] == SELECTED_CONNECTOR_ID
    assert selection["only_approved_json_endpoint_allowed"] is True
    assert approval["connector_id"] == SELECTED_CONNECTOR_ID
    assert approval["production_activation_allowed"] is False
    assert {item["connector"] for item in selection["excluded_connectors"]} >= {"steam", "reddit", "serp"}


def test_missing_opt_in_is_blocked_for_endpoint(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    readiness = endpoint_readiness()
    artifacts = build_live_connector_artifacts()
    assert readiness["status"] == BLOCKED_FOR_ENDPOINT
    assert artifacts["verification"]["status"] == BLOCKED_FOR_ENDPOINT
    assert artifacts["collection"]["real_collection_performed"] is False
    assert artifacts["signals"]["signals"] == []
    assert artifacts["handoff"]["hot_game_candidates"] == []
    assert artifacts["ranking_preview"]["publish_ready"] is False
    assert artifacts["ranking_preview"]["publishing_performed"] is False


def test_live_connector_artifacts_are_json_and_safe() -> None:
    build_live_connector_artifacts()
    unsafe_true = {
        "publishing_performed",
        "raw_response_body_saved",
        "raw_body_saved",
        "deploy_performed",
        "llm_called",
    }
    failures: list[str] = []

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lower = key.lower()
                if lower in unsafe_true and nested is True:
                    failures.append(f"{path}.{key}=true")
                if lower in {"token", "cookie", "api_key", "authorization", "credentials", "raw_response_body"}:
                    if nested not in {False, "[REDACTED]"}:
                        failures.append(f"{path}.{key}")
                walk(nested, f"{path}.{key}")
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                walk(nested, f"{path}[{index}]")

    files = sorted(Path(ARTIFACT_DIR).glob("*.json"))
    assert files
    for path in files:
        walk(json.loads(path.read_text(encoding="utf-8")), path.name)
    assert failures == []


def test_live_connector_api_and_window_are_read_only(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    surface = client.get("/connectors/live")
    window = client.get("/connectors/live-window")
    assert surface.status_code == 200
    assert surface.json()["connector_id"] == SELECTED_CONNECTOR_ID
    assert surface.json()["probe_status"] == BLOCKED_FOR_ENDPOINT
    assert surface.json()["real_collection_performed"] is False
    assert window.status_code == 200
    assert "approved_json_endpoint" in window.text
    assert "Steam, Reddit, JP, KR, SERP" in window.text
