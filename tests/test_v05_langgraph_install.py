import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.v05_langgraph_install.pipeline import ARTIFACT_DIR, command_guardrail, run_batch


client = TestClient(app)


def _load(name: str) -> dict:
    return json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def test_v05_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "explicit_install_approval.json",
        "install_command_guardrail.json",
        "controlled_install_result.json",
        "import_version_probe.json",
        "dependency_state_summary.json",
        "minimal_graph_smoke.json",
        "graph_trace_gate_semantics.json",
        "piko_backend_workflow_smoke.json",
        "operator_langgraph_status.json",
        "real_data_handoff_readiness.json",
    ]
    for name in required:
        assert _load(name)


def test_explicit_approval_and_install_guardrail() -> None:
    run_batch()
    approval = _load("explicit_install_approval.json")
    guardrail = _load("install_command_guardrail.json")

    assert approval["install_approved"] is True
    assert approval["approved_package"] == "langgraph"
    assert approval["production_activation_allowed"] is False
    assert command_guardrail(approval["approved_command"])["allowed"] is True
    assert command_guardrail([sys.executable, "-m", "pip", "install", "langchain"])["allowed"] is False
    assert guardrail["approved_command_probe"]["allowed"] is True
    assert guardrail["disallowed_command_probe"]["allowed"] is False
    assert guardrail["secrets_or_env_dump_saved"] is False


def test_install_import_and_dependency_summary_are_consistent() -> None:
    run_batch()
    install = _load("controlled_install_result.json")
    probe = _load("import_version_probe.json")
    summary = _load("dependency_state_summary.json")

    assert install["install_status"] in {"already_available", "installed", "blocked_for_approval", "blocked_for_dependency"}
    assert install["exit_status"] in {0, None} or isinstance(install["exit_status"], int)
    assert probe["probe_status"] in {"success", "blocked_for_dependency"}
    assert summary["import_success"] is probe["import_success"]
    assert summary["fallback_available"] is True
    if probe["import_success"]:
        assert summary["backend_status"] == "available"
        assert probe["version"] is not None
    else:
        assert summary["backend_status"] == "blocked_for_dependency"


def test_minimal_graph_smoke_and_gate_semantics() -> None:
    run_batch()
    smoke = _load("minimal_graph_smoke.json")
    trace = _load("graph_trace_gate_semantics.json")

    assert smoke["smoke_status"] in {"success", "blocked_for_dependency", "needs_fix"}
    assert smoke["publish_ready"] is False
    assert smoke["llm_used"] is False
    assert trace["gate_decision"] in {"pass", "blocked", "error", "not_run"}
    assert trace["publish_ready"] is False
    if smoke["smoke_status"] != "success":
        assert smoke["backend_ready"] is False
    else:
        assert smoke["backend_ready"] is True


def test_piko_workflow_backend_smoke_and_real_data_handoff_are_safe() -> None:
    run_batch()
    workflow = _load("piko_backend_workflow_smoke.json")
    readiness = _load("real_data_handoff_readiness.json")

    assert workflow["requested_backend"] == "langgraph_backend"
    assert workflow["effective_backend"] in {"langgraph_backend", "local_fixture"}
    assert workflow["verification_required"] is True
    assert workflow["publish_ready"] is False
    assert workflow["publishing_performed"] is False
    assert readiness["real_data_collected"] is False
    assert readiness["production_activation_allowed"] is False
    assert readiness["recommended_real_data_backend"] in {"langgraph_backend", "local_fixture"}


def test_operator_status_api_and_cli_are_read_only() -> None:
    run_batch()
    status = _load("operator_langgraph_status.json")
    api = client.get("/v05/status")
    window = client.get("/v05/langgraph-window")
    cli = subprocess.run(
        [sys.executable, "-m", "packages.v05_langgraph_install.pipeline", "--status"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(cli.stdout)

    assert status["backend_ready"] in {True, False}
    assert api.status_code == 200
    assert api.json()["production_activation_allowed"] is False
    assert api.json()["active_runtime_replaced"] is False
    assert payload["real_source_connector_performed"] is False
    assert window.status_code == 200
    assert "V05 LangGraph Install Smoke" in window.text
    assert "https://" not in window.text


def test_v05_artifacts_do_not_contain_unsafe_side_effects() -> None:
    run_batch()
    unsafe_true_keys = {
        "publish_ready",
        "publishing_performed",
        "deploy_performed",
        "active_runtime_replaced",
        "production_activation_allowed",
        "llm_performed",
        "real_source_connector_performed",
        "credentials_used",
        "vendored_source",
        "real_data_collected",
        "llm_used",
        "external_api_used",
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
