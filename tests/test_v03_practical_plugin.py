import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.v03_practical_plugin.pipeline import ARTIFACT_DIR, run_batch, run_local_graph_fixture


client = TestClient(app)


def _load(name: str) -> dict:
    return json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def test_v03_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "practical_candidate_selection.json",
        "approval_scope_no_install_policy.json",
        "langgraph_style_adapter_contract.json",
        "local_graph_fixture_trace.json",
        "retry_failure_gate_trace.json",
        "discovery_workflow_result.json",
        "article_package_handoff.json",
        "operator_trace_surface.json",
        "real_activation_approval_packet.json",
        "practical_readiness_report.json",
    ]
    for name in required:
        assert _load(name)


def test_candidate_selection_and_no_install_policy_are_safe() -> None:
    run_batch()
    selection = _load("practical_candidate_selection.json")
    policy = _load("approval_scope_no_install_policy.json")

    assert selection["first_candidate"] == "langgraph_style_workflow_adapter"
    assert selection["candidate_only"] is True
    assert selection["auto_install_performed"] is False
    assert selection["active_replacement_performed"] is False
    assert policy["auto_install_allowed"] is False
    assert policy["active_replacement_allowed"] is False
    assert "external_dependency_install" in policy["requires_human_approval"]


def test_langgraph_style_contract_and_local_graph_trace() -> None:
    run_batch()
    contract = _load("langgraph_style_adapter_contract.json")
    trace = _load("local_graph_fixture_trace.json")

    assert contract["backend_required"] is False
    assert contract["optional_backend"] == "langgraph"
    assert contract["side_effect_policy"]["external_install"] is False
    assert contract["side_effect_policy"]["network"] is False
    assert contract["side_effect_policy"]["llm"] is False
    assert contract["nodes"] == ["source_discovery", "evidence_rank", "draft_handoff", "verification_gate"]

    assert trace["status"] == "completed_internal"
    assert [item["node"] for item in trace["trace"]] == contract["nodes"]
    assert trace["state"]["verification"]["status"] == "pass"
    assert trace["publish_ready"] is False
    assert trace["publishing_performed"] is False


def test_retry_failure_gate_semantics_remain_blocked() -> None:
    run_batch()
    failure = _load("retry_failure_gate_trace.json")
    direct = run_local_graph_fixture(force_failure_node="verification_gate")

    assert failure["status"] == "blocked_for_operator"
    assert failure["state"]["verification"]["status"] == "fail"
    gate = failure["state"]["verification"]["gate"]
    assert gate["decision"] == "blocked_for_operator"
    assert gate["next_action"] == "inspect_trace_and_fix_fixture_input"
    assert failure["retry_counts"]["verification_gate"] == 1
    assert direct["status"] == "blocked_for_operator"


def test_discovery_workflow_and_article_handoff_are_internal_only() -> None:
    run_batch()
    workflow = _load("discovery_workflow_result.json")
    handoff = _load("article_package_handoff.json")

    assert workflow["selected_topic"]["decision"] == "publish_candidate"
    assert workflow["ranking_decision"]["watchlist_or_high_risk_promoted"] is False
    assert workflow["publish_ready"] is False
    assert workflow["publishing_performed"] is False
    assert handoff["verification_required"] is True
    assert handoff["article_pipeline_safe_input_shape"] is True
    assert handoff["source_trace"]
    assert handoff["evidence_trace"]
    assert handoff["publish_ready"] is False
    assert handoff["publishing_performed"] is False


def test_operator_surface_activation_packet_and_cli_are_safe() -> None:
    run_batch()
    approval = _load("real_activation_approval_packet.json")
    readiness = _load("practical_readiness_report.json")
    api = client.get("/v03/status")
    window = client.get("/v03/trace-window")
    cli = subprocess.run(
        [sys.executable, "-m", "packages.v03_practical_plugin.pipeline", "--status"],
        check=True,
        capture_output=True,
        text=True,
    )
    cli_payload = json.loads(cli.stdout)

    assert approval["activation_status"] == "not_approved"
    assert approval["auto_activate"] is False
    assert readiness["ready_now"] == "local_fixture_ready"
    assert readiness["not_ready_for_real_external_backend"] is True
    assert api.status_code == 200
    assert api.json()["candidate"] == "langgraph_style_workflow_adapter"
    assert api.json()["active_replacement_performed"] is False
    assert cli_payload["llm_performed"] is False
    assert window.status_code == 200
    assert "V03 LangGraph-style Adapter Trace" in window.text
    assert "Node timeline" in window.text
    assert "Gate decisions" in window.text
    assert "https://" not in window.text


def test_v03_artifacts_do_not_contain_unsafe_side_effects() -> None:
    run_batch()
    unsafe_true_keys = {
        "publish_ready",
        "publishing_performed",
        "auto_install_performed",
        "active_replacement_performed",
        "network_performed",
        "llm_performed",
        "secrets_used",
        "auto_activate",
        "backend_required",
    }
    forbidden_keys = {"api_key", "authorization", "access_token", "refresh_token", "secret", "password"}
    forbidden_phrases = ["pip install", "git clone", "git push"]
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
