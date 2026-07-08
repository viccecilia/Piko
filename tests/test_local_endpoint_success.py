import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.local_endpoint.pipeline import (
    ARTIFACT_DIR,
    LOCAL_SCOPE,
    build_endpoint_artifacts,
    local_endpoint_contract_artifact,
    local_endpoint_fixture_safety_artifact,
    local_endpoint_server,
    local_endpoint_smoke,
    local_opt_in_env,
    run_local_endpoint_success_path,
)
from packages.shared.config import get_settings


client = TestClient(app)


def test_local_endpoint_contract_and_fixture_safety() -> None:
    contract = local_endpoint_contract_artifact()
    safety = local_endpoint_fixture_safety_artifact()
    assert contract["scope"] == LOCAL_SCOPE
    assert contract["broad_internet_coverage"] is False
    assert contract["root_shape_valid"] is True
    assert safety["prohibited_fields_present"] is False
    assert safety["snippet_bounds_ok"] is True
    assert safety["raw_response_body_saved"] is False


def test_local_endpoint_api_returns_approved_json_contract() -> None:
    response = client.get("/local-endpoint/approved-json")
    assert response.status_code == 200
    payload = response.json()
    assert payload["metadata"]["scope"] == LOCAL_SCOPE
    assert payload["metadata"]["broad_internet_coverage"] is False
    assert isinstance(payload["games"], list)
    assert isinstance(payload["questions"], list)


def test_local_opt_in_success_path_sets_env_only_inside_runner(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    assert get_settings().enable_discovery_real_source is False

    with local_endpoint_server() as endpoint_url:
        smoke = local_endpoint_smoke(endpoint_url)
        assert smoke["status_code"] == 200
        assert smoke["contract_valid"] is True
        with local_opt_in_env(endpoint_url):
            assert get_settings().enable_discovery_real_source is True
            assert get_settings().live_discovery_test is True

    assert get_settings().enable_discovery_real_source is False


def test_local_endpoint_live_connector_success_and_handoff(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    artifacts = build_endpoint_artifacts()
    assert artifacts["success"]["status"] == "success"
    assert artifacts["success"]["scope"] == LOCAL_SCOPE
    assert artifacts["success"]["real_collection_performed"] is True
    assert artifacts["success"]["broad_internet_coverage"] is False
    assert artifacts["signals"]["signal_count"] > 0
    assert artifacts["handoff"]["real_collection_performed"] is True
    assert artifacts["handoff"]["source_scope"] == LOCAL_SCOPE
    assert artifacts["handoff"]["top_5_candidates"]
    assert artifacts["handoff"]["pain_buckets"]["hot_answered_questions"]
    assert artifacts["article_handoff"]["verification_required"] is True
    assert artifacts["article_handoff"]["publish_ready"] is False
    assert artifacts["article_handoff"]["publishing_performed"] is False
    assert get_settings().enable_discovery_real_source is False


def test_endpoint_artifacts_parse_and_do_not_store_forbidden_values() -> None:
    build_endpoint_artifacts()
    unsafe_true = {
        "publishing_performed",
        "raw_response_body_saved",
        "raw_body_saved",
        "broad_internet_coverage",
        "crawler_used",
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


def test_endpoint_operator_api_and_window_are_read_only() -> None:
    result = client.get("/local-endpoint/result")
    window = client.get("/local-endpoint/window")
    assert result.status_code == 200
    assert result.json()["scope"] == LOCAL_SCOPE
    assert result.json()["real_collection_performed"] is True
    assert result.json()["broad_internet_coverage"] is False
    assert result.json()["publishing_performed"] is False
    assert window.status_code == 200
    assert "local approved endpoint pilot" in window.text
    assert "Broad internet coverage</dt><dd>false" in window.text
