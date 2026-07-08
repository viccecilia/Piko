import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.v02_runtime.pipeline import (
    ARTIFACT_DIR,
    approval_allows_materialization,
    run_batch,
    run_local_adapter_fixture,
)


client = TestClient(app)


def _load(name: str) -> dict:
    return json.loads((ARTIFACT_DIR / name).read_text(encoding="utf-8"))


def test_v02_batch_generates_required_artifacts() -> None:
    run_batch()
    required = [
        "approval_packet_contract.json",
        "latest_materialization_preview.json",
        "domain_plugin_registry.json",
        "ai_tools_demo_domain_fixture.json",
        "agent_runtime_adapter_contract.json",
        "local_rule_based_adapter_fixture.json",
        "framework_candidate_comparison.json",
        "eval_pack_contract.json",
        "latest_run_trace.json",
        "real_pilot_readiness.json",
    ]
    for name in required:
        assert _load(name)


def test_approval_and_materialization_remain_dry_run() -> None:
    run_batch()
    contract = _load("approval_packet_contract.json")
    pending = contract["sample_pending_packet"]
    allowed, reason = approval_allows_materialization(pending)
    preview = _load("latest_materialization_preview.json")

    assert allowed is False
    assert reason == "approval_not_granted"
    assert preview["materialization_performed"] is False
    assert preview["round_queue_files_created"] is False
    assert preview["safety"]["auto_apply_performed"] is False
    assert preview["safety"]["runtime_adoption_performed"] is False


def test_domain_plugin_registry_and_routes_are_safe() -> None:
    run_batch()
    registry = _load("domain_plugin_registry.json")
    gaming = next(item for item in registry["domains"] if item["domain_id"] == "gaming")
    ai_tools = next(item for item in registry["domains"] if item["domain_id"] == "ai_tools")

    assert gaming["enabled_by_default"] is True
    assert ai_tools["enabled_by_default"] is False
    assert ai_tools["status"] == "candidate"

    domains = client.get("/domains")
    window = client.get("/domains/window")
    unknown = client.get("/domains/unknown")

    assert domains.status_code == 200
    assert domains.json()["publish_ready"] is False
    assert window.status_code == 200
    assert "Domain Routing" in window.text
    assert "https://" not in window.text
    assert unknown.json()["routing_decision"] == "safe_fail_unknown_domain"


def test_adapter_eval_trace_and_readiness_contracts() -> None:
    run_batch()
    adapter_contract = _load("agent_runtime_adapter_contract.json")
    eval_pack = _load("eval_pack_contract.json")
    trace = _load("latest_run_trace.json")
    readiness = _load("real_pilot_readiness.json")

    assert adapter_contract["tool_policy"]["network_default"] is False
    assert adapter_contract["side_effect_policy"]["active_runtime_replacement_allowed"] is False
    assert len(eval_pack["checks"]) >= 5
    assert eval_pack["verification_bypass_allowed"] is False
    assert "authorization" not in json.dumps(trace).lower()
    assert "raw_text" not in json.dumps(trace).lower()
    assert trace["publishing_performed"] is False
    assert readiness["real_collection_performed"] is False
    assert readiness["live_success_claimed"] is False

    ok = run_local_adapter_fixture({"task_id": "ok", "claim": "Use trace", "source_ids": ["fixture_source_001"]})
    bad = run_local_adapter_fixture({"task_id": "bad", "claim": "Unsupported", "source_ids": [], "unsupported_claim": True})
    assert ok["verification_report"]["status"] == "pass"
    assert bad["verification_report"]["status"] == "fail"
    assert ok["llm_used"] is False
    assert ok["external_framework_used"] is False


def test_operator_trace_window_and_cli_are_read_only() -> None:
    run_batch()
    cli = subprocess.run(
        [sys.executable, "-m", "packages.v02_runtime.pipeline", "--status"],
        check=True,
        capture_output=True,
        text=True,
    )
    status = json.loads(cli.stdout)
    window = client.get("/operator/trace-window")

    assert status["approval_required"] is True
    assert status["materialization_performed"] is False
    assert status["active_runtime_replaced"] is False
    assert status["network_performed"] is False
    assert status["llm_performed"] is False
    assert window.status_code == 200
    assert "Trace" in window.text
    assert "Gate" in window.text
    assert "Verification" in window.text
    assert "Human approval" in window.text
    assert "https://" not in window.text


def test_v02_artifacts_do_not_contain_unsafe_side_effects() -> None:
    run_batch()
    unsafe_true_keys = {
        "publish_ready",
        "publishing_performed",
        "materialization_performed",
        "auto_apply_performed",
        "runtime_adoption_performed",
        "network_performed",
        "llm_performed",
        "installed",
        "active_runtime_replaced",
    }
    forbidden_keys = {"api_key", "authorization", "access_token", "refresh_token", "secret", "password", "raw_text"}
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

    for artifact in Path(ARTIFACT_DIR).glob("*.json"):
        walk(json.loads(artifact.read_text(encoding="utf-8")), artifact.name)

    assert failures == []
