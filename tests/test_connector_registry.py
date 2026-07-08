import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.connector_registry.pipeline import (
    ARTIFACT_DIR,
    build_connector_artifacts,
    build_connector_registry,
    build_permission_audit_policy,
    credential_policy,
    plan_collection,
    route_connector,
    validate_connector_manifest,
)


client = TestClient(app)


def test_connector_registry_contract_is_domain_agnostic_and_disabled() -> None:
    registry = build_connector_registry()
    assert registry["domain_agnostic"] is True
    assert registry["default_mode"] == "dry_run"
    assert registry["real_collection_performed"] is False
    for connector in registry["connectors"]:
        assert validate_connector_manifest(connector) == []
        assert connector["approval_required"] is True
        assert connector["dry_run_supported"] is True
        assert connector["live_collect_default"] is False


def test_credential_policy_redacts_sensitive_keys() -> None:
    policy = credential_policy()
    text = json.dumps(policy).lower()
    assert policy["credential_storage_allowed"] is False
    assert policy["sanitized_probe"]["token"] == "[REDACTED]"
    assert policy["sanitized_probe"]["nested"]["authorization"] == "[REDACTED]"
    assert "redaction_probe" not in text


def test_permission_audit_denies_live_collect_by_default() -> None:
    policy = build_permission_audit_policy()
    for row in policy["permissions"]:
        assert row["allowed_operations"] == ["dry_run", "verify_contract"]
        assert "live_collect" in row["denied_operations"]
    assert policy["live_collect_default_allowed"] is False


def test_domain_connector_packs_and_routing_are_safe() -> None:
    artifacts = build_connector_artifacts()
    gaming_pack = artifacts["gaming_pack"]
    ai_pack = artifacts["ai_tools_pack"]
    assert gaming_pack["all_live_connectors_disabled_by_default"] is True
    assert ai_pack["github_api_called"] is False
    assert ai_pack["repo_source_vendored"] is False
    assert route_connector("gaming")["status"] == "matched"
    assert route_connector("ai_tools")["status"] == "matched"
    assert route_connector("unknown")["status"] == "safe_fail"


def test_collection_plan_and_dry_run_report_do_not_collect() -> None:
    artifacts = build_connector_artifacts()
    gaming_plan = plan_collection("gaming", "hot needs")
    ai_plan = plan_collection("ai_tools", "tool selection")
    report = artifacts["dry_run_report"]
    assert gaming_plan["mode"] == "dry_run"
    assert ai_plan["mode"] == "dry_run"
    assert gaming_plan["real_collection_performed"] is False
    assert report["no_network_performed"] is True
    assert report["real_collection_performed"] is False
    assert report["real_status"]["status"] == "blocked_for_endpoint"


def test_connector_api_and_window_are_read_only() -> None:
    build_connector_artifacts()
    surface = client.get("/connectors")
    window = client.get("/connectors/window")
    route = client.get("/connectors/route?domain_id=ai_tools")
    plan = client.post("/connectors/plan?domain_id=gaming&target_need=save_location")
    assert surface.status_code == 200
    assert surface.json()["real_collection_performed"] is False
    assert window.status_code == 200
    assert "Connector Registry" in window.text
    assert "https://" not in window.text
    assert route.json()["live_collect_allowed"] is False
    assert plan.json()["no_network_performed"] is True


def test_connector_artifacts_parse_and_do_not_store_unsafe_fields() -> None:
    build_connector_artifacts()
    forbidden_keys = {
        "token",
        "cookie",
        "api_key",
        "authorization",
        "credentials",
        "access_token",
        "refresh_token",
        "secret",
        "password",
        "raw_text",
        "raw_body",
        "raw_response_body",
    }
    unsafe_true = {"real_collection_performed", "publishing_performed", "dispatch_performed", "upload_performed", "network_performed"}
    failures: list[str] = []

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lower = key.lower()
                if lower in forbidden_keys and nested not in {"[REDACTED]", False}:
                    failures.append(f"{path}.{key}")
                if lower in unsafe_true and nested is True:
                    failures.append(f"{path}.{key}=true")
                walk(nested, f"{path}.{key}")
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                walk(nested, f"{path}[{index}]")

    for path in Path(ARTIFACT_DIR).glob("*.json"):
        walk(json.loads(path.read_text(encoding="utf-8")), path.name)

    assert failures == []
