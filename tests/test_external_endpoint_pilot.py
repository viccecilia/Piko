import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.external_endpoint.pipeline import (
    ARTIFACT_DIR,
    BLOCKED,
    EXTERNAL_SCOPE,
    build_external_endpoint_artifacts,
    external_endpoint_approval_contract,
    external_endpoint_readiness,
    validate_external_payload_contract,
)
from packages.shared.config import get_settings


client = TestClient(app)


def test_external_endpoint_approval_contract_is_bounded() -> None:
    approval = external_endpoint_approval_contract()
    assert approval["endpoint_required"] is True
    assert approval["endpoint_type"] == "json"
    assert approval["operator_approved_required"] is True
    assert approval["allowed_scope"] == EXTERNAL_SCOPE
    assert approval["broad_internet_coverage"] is False
    assert "crawler" in approval["rejected_endpoint_types"]


def test_missing_external_endpoint_is_blocked(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    readiness = external_endpoint_readiness()
    artifacts = build_external_endpoint_artifacts()
    assert readiness["status"] == BLOCKED
    assert artifacts["probe"]["status"] == BLOCKED
    assert artifacts["probe"]["real_collection_performed"] is False
    assert artifacts["signals"]["signals"] == []
    assert artifacts["handoff"]["top_candidates"] == []
    assert artifacts["candidate_package"]["publish_ready"] is False


def test_localhost_url_is_not_external_success(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_APPROVED_ENDPOINT_URL", "http://127.0.0.1:9999/local-approved-endpoint.json")
    get_settings.cache_clear()
    readiness = external_endpoint_readiness()
    assert readiness["status"] == BLOCKED
    assert readiness["blocked_reason"] == "localhost_not_allowed_for_external_endpoint"
    assert readiness["real_collection_performed"] is False
    get_settings.cache_clear()


def test_invalid_payload_contract_returns_failed_contract_validation() -> None:
    result = validate_external_payload_contract({"games": []})
    assert result["status"] == "failed_contract_validation"
    assert result["real_collection_performed"] is False


def test_external_endpoint_artifacts_parse_and_are_safe(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    build_external_endpoint_artifacts()
    unsafe_true = {
        "publishing_performed",
        "publish_ready",
        "raw_response_body_saved",
        "full_posts_saved",
        "full_pages_saved",
        "full_comments_saved",
        "secrets_retained",
        "crawler_used",
        "html_scrape_used",
        "broad_internet_coverage",
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


def test_external_endpoint_operator_api_and_window_are_read_only(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    result = client.get("/external-endpoint/result")
    window = client.get("/external-endpoint/window")
    assert result.status_code == 200
    assert result.json()["scope"] == EXTERNAL_SCOPE
    assert result.json()["status"] == BLOCKED
    assert result.json()["real_collection_performed"] is False
    assert result.json()["broad_internet_coverage"] is False
    assert result.json()["publishing_performed"] is False
    assert window.status_code == 200
    assert "not broad internet coverage" in window.text
