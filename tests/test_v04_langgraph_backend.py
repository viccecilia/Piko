import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.v04_langgraph_backend.pipeline import ARTIFACT_DIR, run_batch, select_backend


client = TestClient(app)


def _load(name: str) -> dict:
    return json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def test_v04_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "dependency_license_safety_review.json",
        "explicit_pilot_approval.json",
        "dependency_availability_probe.json",
        "install_path_or_safe_block.json",
        "backend_probe_summary.json",
        "backend_selector_contract.json",
        "langgraph_backend_adapter_shape.json",
        "backend_smoke_workflow.json",
        "operator_backend_status.json",
        "activation_readiness.json",
    ]
    for name in required:
        assert _load(name)


def test_dependency_review_and_approval_do_not_allow_production_or_install() -> None:
    run_batch()
    review = _load("dependency_license_safety_review.json")
    approval = _load("explicit_pilot_approval.json")

    assert review["review_status"] == "pilot_review_only"
    assert review["production_approved"] is False
    assert review["license_review"]["production_approved"] is False
    assert approval["pilot_approved"] is True
    assert approval["dependency_probe_allowed"] is True
    assert approval["install_allowed"] is False
    assert approval["network_allowed"] is False
    assert approval["llm_allowed"] is False
    assert approval["production_activation_allowed"] is False


def test_dependency_probe_and_install_path_are_explicit_about_blocked_or_available() -> None:
    run_batch()
    probe = _load("dependency_availability_probe.json")
    install = _load("install_path_or_safe_block.json")
    summary = _load("backend_probe_summary.json")

    assert probe["backend_status"] in {"available", "blocked_for_dependency", "blocked_for_approval"}
    assert probe["install_performed"] is False
    assert install["install_allowed"] is False
    assert install["install_performed"] is False
    assert install["status"] == "blocked_for_approval"
    assert summary["fallback_available"] is True
    assert summary["fallback_backend"] == "local_fixture"
    if not probe["langgraph_available"]:
        assert summary["backend_status"] in {"blocked_for_dependency", "blocked_for_approval"}


def test_backend_selector_defaults_to_local_fixture_and_blocks_unavailable_backend() -> None:
    run_batch()
    selector = _load("backend_selector_contract.json")
    default = select_backend("local_fixture")
    langgraph = select_backend("langgraph_backend")

    assert selector["default_backend"] == "local_fixture"
    assert selector["production_config_modified"] is False
    assert default["effective_backend"] == "local_fixture"
    assert langgraph["effective_backend"] in {"local_fixture", "langgraph_backend"}
    if langgraph["effective_backend"] == "local_fixture":
        assert langgraph["backend_status"] in {"blocked_for_dependency", "blocked_for_approval"}


def test_backend_adapter_and_smoke_do_not_replace_runtime_or_publish() -> None:
    run_batch()
    adapter = _load("langgraph_backend_adapter_shape.json")
    smoke = _load("backend_smoke_workflow.json")
    readiness = _load("activation_readiness.json")

    assert adapter["contract_compatible"] is True
    assert adapter["effective_backend"] in {"local_fixture", "langgraph_backend"}
    assert smoke["requested_backend"] == "langgraph_backend"
    assert smoke["effective_backend"] in {"local_fixture", "langgraph_backend"}
    assert smoke["publish_ready"] is False
    assert smoke["publishing_performed"] is False
    assert smoke["deploy_performed"] is False
    assert readiness["production_activation_allowed"] is False
    assert readiness["active_runtime_replaced"] is False


def test_operator_surface_and_cli_are_read_only() -> None:
    run_batch()
    api = client.get("/v04/status")
    window = client.get("/v04/backend-window")
    cli = subprocess.run(
        [sys.executable, "-m", "packages.v04_langgraph_backend.pipeline", "--status"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(cli.stdout)

    assert api.status_code == 200
    assert api.json()["activation_status"] == "not_approved_for_production"
    assert api.json()["active_runtime_replaced"] is False
    assert payload["production_activation_allowed"] is False
    assert payload["active_runtime_replaced"] is False
    assert window.status_code == 200
    assert "V04 LangGraph Backend Pilot" in window.text
    assert "Backend status" in window.text
    assert "https://" not in window.text


def test_v04_artifacts_do_not_contain_unsafe_side_effects() -> None:
    run_batch()
    unsafe_true_keys = {
        "publish_ready",
        "publishing_performed",
        "deploy_performed",
        "active_runtime_replaced",
        "production_activation_allowed",
        "llm_performed",
        "external_connector_performed",
        "credentials_used",
        "vendored_source",
        "install_performed",
        "network_allowed",
        "llm_allowed",
    }
    forbidden_keys = {"api_key", "authorization", "access_token", "refresh_token", "secret", "password"}
    forbidden_phrases = ["git clone", "git push", "deploy performed", "published"]
    failures: list[str] = []

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                lower = key.lower()
                if lower in forbidden_keys:
                    failures.append(f"{path}.{key}")
                if lower in unsafe_true_keys and nested is True:
                    failures.append(f"{path}.{key}=true")
                walk(nested, f"{path}.{key}")
        elif isinstance(value, list):
            for index, nested in enumerate(value):
                walk(nested, f"{path}[{index}]")
        elif isinstance(value, str):
            lowered = value.lower()
            for phrase in forbidden_phrases:
                if phrase in lowered:
                    failures.append(f"{path} contains {phrase}")

    for artifact in Path(ARTIFACT_DIR).glob("*.json"):
        walk(json.loads(artifact.read_text(encoding="utf-8")), artifact.name)

    assert failures == []
