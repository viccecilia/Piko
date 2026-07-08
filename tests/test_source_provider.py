import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.discovery.real_endpoint_contract import validate_approved_endpoint_payload
from packages.source_provider.pipeline import (
    ARTIFACT_DIR,
    PAYLOAD_PATH,
    approved_payload_package_artifact,
    build_source_provider_artifacts,
    external_url_validation_artifact,
    package_manifest_artifact,
    provider_approval_contract,
    provider_strategy_artifact,
    static_endpoint_package_artifact,
)


client = TestClient(app)


def test_provider_strategy_and_approval_contract_are_safe() -> None:
    strategy = provider_strategy_artifact()
    approval = provider_approval_contract()
    assert strategy["recommended_strategy"] == "static_json_provider_package_first"
    assert "localhost" in strategy["invalid_external_providers"]
    assert "file" in strategy["invalid_external_providers"]
    assert approval["external_url_required"] is True
    assert approval["operator_approval_required"] is True
    assert approval["credential_storage_allowed"] is False
    assert approval["deployment_allowed"] is False
    assert approval["publishing_performed"] is False
    assert approval["external_provider_validated"] is False


def test_approved_payload_and_static_package_are_contract_valid() -> None:
    payload_artifact = approved_payload_package_artifact()
    package = static_endpoint_package_artifact()
    payload = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
    validation = validate_approved_endpoint_payload(payload)
    assert payload_artifact["contract_valid"] is True
    assert package["contract_valid"] is True
    assert validation["status"] == "valid"
    assert payload["metadata"]["provider_package_scope"] == "deploy_ready_static_json"
    assert payload["metadata"]["external_provider_validated"] is False
    assert package["deployment_performed"] is False
    assert package["credentials_stored"] is False
    assert Path(package["readme_path"]).read_text(encoding="utf-8").count("API key") == 1


def test_package_manifest_hash_matches_payload() -> None:
    manifest = package_manifest_artifact()
    digest = hashlib.sha256(PAYLOAD_PATH.read_bytes()).hexdigest()
    assert manifest["payload_hash_sha256"] == digest
    assert manifest["safety_flags"]["raw_body_saved"] is False
    assert manifest["safety_flags"]["secrets_retained"] is False
    assert manifest["safety_flags"]["upload_performed"] is False
    assert manifest["safety_flags"]["deployment_performed"] is False
    assert manifest["safety_flags"]["broad_internet_coverage"] is False


def test_no_external_url_is_deploy_ready_pending_host(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_EXTERNAL_APPROVED_ENDPOINT_URL", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    result = external_url_validation_artifact()
    assert result["status"] == "deploy_ready_pending_host"
    assert result["external_provider_validated"] is False
    assert result["real_collection_performed"] is False
    assert result["raw_response_body_saved"] is False


def test_localhost_url_is_rejected_as_non_external(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_EXTERNAL_APPROVED_ENDPOINT_URL", "http://127.0.0.1:7777/approved-market.json")
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    result = external_url_validation_artifact()
    assert result["status"] == "blocked_for_external_url"
    assert result["blocked_reason"] == "localhost_not_external"
    assert result["external_provider_validated"] is False
    assert result["real_collection_performed"] is False


def test_source_provider_artifacts_parse_and_do_not_store_forbidden_values(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_EXTERNAL_APPROVED_ENDPOINT_URL", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    build_source_provider_artifacts()
    failures: list[str] = []
    unsafe_true = {
        "credential_storage_allowed",
        "deployment_allowed",
        "deployment_performed",
        "upload_performed",
        "publishing_performed",
        "raw_response_body_saved",
        "raw_body_saved",
        "secrets_retained",
        "broad_internet_coverage",
        "external_provider_validated",
    }
    forbidden_keys = {"token", "cookie", "api_key", "authorization", "credentials", "raw_response_body"}

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lower = key.lower()
                if lower in unsafe_true and nested is True:
                    failures.append(f"{path}.{key}=true")
                if lower in forbidden_keys and nested not in {False, "[REDACTED]"}:
                    failures.append(f"{path}.{key}")
                walk(nested, f"{path}.{key}")
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                walk(nested, f"{path}[{index}]")

    files = sorted(Path(ARTIFACT_DIR).glob("*.json")) + sorted((ARTIFACT_DIR / "static_endpoint_package").glob("*.json"))
    assert files
    for path in files:
        walk(json.loads(path.read_text(encoding="utf-8")), path.name)
    assert failures == []


def test_source_provider_operator_api_and_window_are_read_only(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_EXTERNAL_APPROVED_ENDPOINT_URL", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    result = client.get("/source-provider/result")
    window = client.get("/source-provider/window")
    assert result.status_code == 200
    payload = result.json()
    assert payload["provider_status"] == "deploy_ready_pending_host"
    assert payload["external_provider_validated"] is False
    assert payload["upload_performed"] is False
    assert payload["deployment_performed"] is False
    assert payload["publishing_performed"] is False
    assert window.status_code == 200
    assert "No upload or deployment was performed" in window.text
    assert "External provider validated</dt><dd>false" in window.text
