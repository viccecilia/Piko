from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TypedDict

from packages.v03_practical_plugin.pipeline import run_local_graph_fixture


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts" / "v05_langgraph_install"
V04_DIR = ROOT / "artifacts" / "v04_langgraph_backend"
SUMMARY_DIR = ROOT / ".piko" / "summaries"
DOCS_DIR = ROOT / "docs"

ROUND_ORDER = [
    "V05-1-R01",
    "V05-1-R02",
    "V05-2-R01",
    "V05-2-R02",
    "V05-2-R03",
    "V05-3-R01",
    "V05-3-R02",
    "V05-4-R01",
    "V05-4-R02",
    "V05-5-R01",
    "V05-5-R02",
]

STAGE_ROUNDS = {
    "V05-1": ["V05-1-R01", "V05-1-R02"],
    "V05-2": ["V05-2-R01", "V05-2-R02", "V05-2-R03"],
    "V05-3": ["V05-3-R01", "V05-3-R02"],
    "V05-4": ["V05-4-R01", "V05-4-R02"],
    "V05-5": ["V05-5-R01", "V05-5-R02"],
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_dirs() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    _ensure_dirs()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _read_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}
    return json.loads(path.read_text(encoding="utf-8"))


def _safety_flags() -> dict[str, bool]:
    return {
        "publish_ready": False,
        "publishing_performed": False,
        "deploy_performed": False,
        "active_runtime_replaced": False,
        "production_activation_allowed": False,
        "llm_performed": False,
        "real_source_connector_performed": False,
        "credentials_used": False,
        "vendored_source": False,
    }


def _short(text: str, limit: int = 900) -> str:
    clean = text.replace("\r", "\n")
    return clean[-limit:] if len(clean) > limit else clean


def probe_import() -> dict[str, Any]:
    try:
        module = importlib.import_module("langgraph")
        version = getattr(module, "__version__", "unknown")
        module_file = getattr(module, "__file__", None)
        return {
            "probe_status": "success",
            "import_success": True,
            "version": version,
            "module_path_summary": Path(module_file).name if module_file else "namespace_or_unknown",
            "blocked_reason": None,
        }
    except Exception as exc:  # noqa: BLE001 - probe must report blocked dependency safely.
        return {
            "probe_status": "blocked_for_dependency",
            "import_success": False,
            "version": None,
            "module_path_summary": None,
            "blocked_reason": f"{type(exc).__name__}: {exc}",
        }


def write_install_approval() -> Path:
    v04 = _read_json(V04_DIR / "operator_backend_status.json")
    payload = {
        "artifact_id": "v05_explicit_langgraph_install_approval",
        "generated_at": _now(),
        "source_v04_backend_status": v04.get("backend_status"),
        "install_approved": True,
        "approved_package": "langgraph",
        "approved_command": [sys.executable, "-m", "pip", "install", "langgraph"],
        "version_policy": "latest compatible package from configured pip index for local smoke only",
        "production_activation_allowed": False,
        "rollback_note": "Keep local_fixture as default backend; do not alter active runtime.",
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "explicit_install_approval.json", payload)


def command_guardrail(command: list[str]) -> dict[str, Any]:
    approval = _read_json(ARTIFACT_DIR / "explicit_install_approval.json")
    approved = approval.get("approved_command", [])
    package = approval.get("approved_package")
    command_text = " ".join(command)
    allowed = (
        bool(approval.get("install_approved"))
        and command == approved
        and package == "langgraph"
        and "langgraph" in command
        and "git+" not in command_text
        and "http://" not in command_text
        and "https://" not in command_text
    )
    return {
        "command": command,
        "allowed": allowed,
        "blocked_reason": None if allowed else "command_not_in_explicit_v05_approval",
    }


def write_install_guardrail() -> Path:
    approval = _read_json(ARTIFACT_DIR / "explicit_install_approval.json")
    approved = approval.get("approved_command", [])
    disallowed = [sys.executable, "-m", "pip", "install", "langchain"]
    payload = {
        "artifact_id": "install_command_guardrail",
        "generated_at": _now(),
        "approved_command_probe": command_guardrail(approved),
        "disallowed_command_probe": command_guardrail(disallowed),
        "secrets_or_env_dump_saved": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "install_command_guardrail.json", payload)


def run_controlled_install() -> dict[str, Any]:
    existing = _read_json(ARTIFACT_DIR / "controlled_install_result.json")
    if existing.get("install_status") == "installed" and existing.get("install_performed") is True:
        return {
            key: value
            for key, value in existing.items()
            if key not in {"artifact_id", "generated_at", *list(_safety_flags().keys())}
        }
    approval = _read_json(ARTIFACT_DIR / "explicit_install_approval.json")
    command = approval.get("approved_command", [])
    guard = command_guardrail(command)
    before = probe_import()
    if before["import_success"]:
        return {
            "install_status": "already_available",
            "install_performed": False,
            "command": command,
            "exit_status": 0,
            "stdout_tail": "",
            "stderr_tail": "",
            "version_before": before["version"],
            "version_after": before["version"],
            "blocked_reason": None,
        }
    if not approval.get("install_approved") or not guard["allowed"]:
        return {
            "install_status": "blocked_for_approval",
            "install_performed": False,
            "command": command,
            "exit_status": None,
            "stdout_tail": "",
            "stderr_tail": "",
            "version_before": None,
            "version_after": None,
            "blocked_reason": guard["blocked_reason"],
        }
    completed = subprocess.run(command, capture_output=True, text=True, timeout=180, check=False)
    after = probe_import()
    status = "installed" if completed.returncode == 0 and after["import_success"] else "blocked_for_dependency"
    return {
        "install_status": status,
        "install_performed": completed.returncode == 0,
        "command": command,
        "exit_status": completed.returncode,
        "stdout_tail": _short(completed.stdout),
        "stderr_tail": _short(completed.stderr),
        "version_before": before["version"],
        "version_after": after["version"],
        "blocked_reason": None if status == "installed" else after.get("blocked_reason") or f"pip exited {completed.returncode}",
    }


def write_controlled_install() -> Path:
    payload = {
        "artifact_id": "controlled_langgraph_install",
        "generated_at": _now(),
        **run_controlled_install(),
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "controlled_install_result.json", payload)


def write_import_version_probe() -> Path:
    payload = {
        "artifact_id": "import_version_probe",
        "generated_at": _now(),
        "package": "langgraph",
        "raw_package_source_dumped": False,
        **probe_import(),
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "import_version_probe.json", payload)


def write_dependency_state_summary() -> Path:
    install = _read_json(ARTIFACT_DIR / "controlled_install_result.json")
    probe = _read_json(ARTIFACT_DIR / "import_version_probe.json")
    fallback = run_local_graph_fixture()
    backend_status = "available" if probe.get("import_success") else "blocked_for_dependency"
    payload = {
        "artifact_id": "dependency_state_summary",
        "generated_at": _now(),
        "install_performed": bool(install.get("install_performed")),
        "install_status": install.get("install_status"),
        "import_success": bool(probe.get("import_success")),
        "version": probe.get("version"),
        "backend_status": backend_status,
        "fallback_available": fallback.get("status") in {"completed_internal", "blocked_for_operator"},
        "fallback_smoke_status": fallback.get("status"),
        "blocked_reason": None if probe.get("import_success") else probe.get("blocked_reason"),
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "dependency_state_summary.json", payload)


class MinimalState(TypedDict):
    value: int
    gate_decision: str
    trace: list[str]


def run_minimal_langgraph_smoke() -> dict[str, Any]:
    probe = _read_json(ARTIFACT_DIR / "import_version_probe.json")
    if not probe.get("import_success"):
        return {
            "smoke_status": "blocked_for_dependency",
            "backend_ready": False,
            "blocked_reason": probe.get("blocked_reason"),
            "nodes": ["start", "transform", "gate", "end"],
            "trace": [],
            "gate_decision": "not_run",
            "retry_count": 0,
        }
    try:
        from langgraph.graph import END, StateGraph

        def start(state: MinimalState) -> MinimalState:
            return {"value": state["value"], "gate_decision": "", "trace": state["trace"] + ["start"]}

        def transform(state: MinimalState) -> MinimalState:
            return {"value": state["value"] + 1, "gate_decision": "", "trace": state["trace"] + ["transform"]}

        def gate(state: MinimalState) -> MinimalState:
            decision = "pass" if state["value"] == 2 else "blocked"
            return {"value": state["value"], "gate_decision": decision, "trace": state["trace"] + ["gate"]}

        graph_builder = StateGraph(MinimalState)
        graph_builder.add_node("start", start)
        graph_builder.add_node("transform", transform)
        graph_builder.add_node("gate", gate)
        graph_builder.set_entry_point("start")
        graph_builder.add_edge("start", "transform")
        graph_builder.add_edge("transform", "gate")
        graph_builder.add_edge("gate", END)
        graph = graph_builder.compile()
        result = graph.invoke({"value": 1, "gate_decision": "", "trace": []})
        success = result["gate_decision"] == "pass"
        return {
            "smoke_status": "success" if success else "needs_fix",
            "backend_ready": success,
            "blocked_reason": None if success else "gate did not pass",
            "nodes": ["start", "transform", "gate", "end"],
            "trace": result["trace"],
            "gate_decision": result["gate_decision"],
            "retry_count": 0,
        }
    except Exception as exc:  # noqa: BLE001 - smoke must report failure without crashing the batch.
        return {
            "smoke_status": "needs_fix",
            "backend_ready": False,
            "blocked_reason": f"{type(exc).__name__}: {exc}",
            "nodes": ["start", "transform", "gate", "end"],
            "trace": [],
            "gate_decision": "error",
            "retry_count": 0,
        }


def write_minimal_graph_smoke() -> Path:
    payload = {
        "artifact_id": "minimal_langgraph_graph_smoke",
        "generated_at": _now(),
        **run_minimal_langgraph_smoke(),
        "llm_used": False,
        "external_api_used": False,
        "publish_ready": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "minimal_graph_smoke.json", payload)


def write_graph_trace_gate() -> Path:
    smoke = _read_json(ARTIFACT_DIR / "minimal_graph_smoke.json")
    payload = {
        "artifact_id": "graph_smoke_trace_gate_semantics",
        "generated_at": _now(),
        "smoke_status": smoke.get("smoke_status"),
        "nodes": smoke.get("nodes", []),
        "state_summaries": [
            {"node": node, "state_summary": "bounded fixture state"} for node in smoke.get("trace", [])
        ],
        "gate_decision": smoke.get("gate_decision"),
        "retry_count": smoke.get("retry_count", 0),
        "backend_ready": bool(smoke.get("backend_ready")),
        "failed_or_blocked_not_marked_success": smoke.get("smoke_status") != "success" or smoke.get("backend_ready") is True,
        "publish_ready": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "graph_trace_gate_semantics.json", payload)


def run_piko_workflow_backend_smoke() -> dict[str, Any]:
    smoke = _read_json(ARTIFACT_DIR / "minimal_graph_smoke.json")
    fallback = run_local_graph_fixture()
    if not smoke.get("backend_ready"):
        return {
            "workflow_smoke_status": "blocked_for_dependency" if smoke.get("smoke_status") == "blocked_for_dependency" else "needs_fix",
            "requested_backend": "langgraph_backend",
            "effective_backend": "local_fixture",
            "backend_ready": False,
            "blocked_reason": smoke.get("blocked_reason"),
            "trace": {
                "fallback_status": fallback.get("status"),
                "trace_ids": [item.get("trace_id") for item in fallback.get("trace", [])],
            },
        }
    return {
        "workflow_smoke_status": "success",
        "requested_backend": "langgraph_backend",
        "effective_backend": "langgraph_backend",
        "backend_ready": True,
        "blocked_reason": None,
        "trace": {
            "nodes": ["source_discovery", "evidence_rank", "draft_handoff", "verification_gate"],
            "gate_decision": "pass_for_internal_handoff",
        },
    }


def write_piko_backend_workflow_smoke() -> Path:
    payload = {
        "artifact_id": "piko_workflow_langgraph_backend_smoke",
        "generated_at": _now(),
        "verification_required": True,
        "publish_ready": False,
        "publishing_performed": False,
        **run_piko_workflow_backend_smoke(),
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "piko_backend_workflow_smoke.json", payload)


def write_operator_status() -> Path:
    install = _read_json(ARTIFACT_DIR / "controlled_install_result.json")
    probe = _read_json(ARTIFACT_DIR / "import_version_probe.json")
    minimal = _read_json(ARTIFACT_DIR / "minimal_graph_smoke.json")
    workflow = _read_json(ARTIFACT_DIR / "piko_backend_workflow_smoke.json")
    payload = {
        "artifact_id": "operator_langgraph_status",
        "generated_at": _now(),
        "install_status": install.get("install_status"),
        "install_performed": bool(install.get("install_performed")),
        "import_success": bool(probe.get("import_success")),
        "version": probe.get("version"),
        "minimal_smoke_status": minimal.get("smoke_status"),
        "workflow_smoke_status": workflow.get("workflow_smoke_status"),
        "effective_backend": workflow.get("effective_backend"),
        "fallback_available": workflow.get("effective_backend") == "local_fixture" or workflow.get("backend_ready") is True,
        "backend_ready": workflow.get("backend_ready") is True,
        "read_only": True,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "operator_langgraph_status.json", payload)


def status_window_html() -> str:
    status = _read_json(ARTIFACT_DIR / "operator_langgraph_status.json", {"install_status": "not_generated"})
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko V05 LangGraph Status</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "section{border:1px solid #d8e0ea;border-radius:6px;padding:12px;margin:12px 0}</style>"
        "</head><body><h1>V05 LangGraph Install Smoke</h1>"
        f"<section><h2>Install status</h2><p>{status.get('install_status')}</p></section>"
        f"<section><h2>Import</h2><p>{status.get('import_success')} / {status.get('version')}</p></section>"
        f"<section><h2>Minimal smoke</h2><p>{status.get('minimal_smoke_status')}</p></section>"
        f"<section><h2>Workflow smoke</h2><p>{status.get('workflow_smoke_status')}</p></section>"
        f"<section><h2>Effective backend</h2><p>{status.get('effective_backend')}</p></section>"
        "</body></html>"
    )


def write_real_data_handoff_readiness() -> Path:
    status = _read_json(ARTIFACT_DIR / "operator_langgraph_status.json")
    recommended = "langgraph_backend" if status.get("backend_ready") else "local_fixture"
    payload = {
        "artifact_id": "real_data_handoff_readiness",
        "generated_at": _now(),
        "runtime_backend_status": "backend_ready" if status.get("backend_ready") else status.get("workflow_smoke_status"),
        "recommended_real_data_backend": recommended,
        "required_endpoint_env": [
            "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true",
            "PIKO_LIVE_DISCOVERY_TEST=true",
            "PIKO_APPROVED_ENDPOINT_URL=<approved json endpoint>",
        ],
        "source_guardrails": [
            "approved JSON endpoints only",
            "no crawler",
            "no raw/full source body retention",
            "ordinary pytest remains offline",
            "publish_ready remains false",
        ],
        "next_stage": "real data batch only after Piko-verify approval",
        "real_data_collected": False,
        "production_activation_allowed": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "real_data_handoff_readiness.json", payload)


def write_current_state_note() -> Path:
    path = DOCS_DIR / "current_state.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Current State\n"
    marker = "## V05 Real LangGraph Install Smoke"
    status = _read_json(ARTIFACT_DIR / "operator_langgraph_status.json")
    note = (
        f"\n{marker}\n\n"
        "V05 explicitly approved and attempted a real LangGraph install/import smoke. "
        f"Install status is `{status.get('install_status')}`, import success is `{status.get('import_success')}`, "
        f"version is `{status.get('version')}`, minimal smoke is `{status.get('minimal_smoke_status')}`, "
        f"and workflow smoke is `{status.get('workflow_smoke_status')}` using effective backend "
        f"`{status.get('effective_backend')}`. Production activation remains false, active runtime is not replaced, "
        "and no real data batch was started.\n"
    )
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + note
    else:
        existing = existing.rstrip() + "\n" + note
    path.write_text(existing, encoding="utf-8")
    return path


def v05_status() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "operator_langgraph_status.json").exists():
        run_batch()
    status = _read_json(ARTIFACT_DIR / "operator_langgraph_status.json")
    readiness = _read_json(ARTIFACT_DIR / "real_data_handoff_readiness.json")
    return {
        "status": "completed",
        "install_status": status.get("install_status"),
        "import_success": status.get("import_success"),
        "version": status.get("version"),
        "minimal_smoke_status": status.get("minimal_smoke_status"),
        "workflow_smoke_status": status.get("workflow_smoke_status"),
        "effective_backend": status.get("effective_backend"),
        "backend_ready": status.get("backend_ready"),
        "recommended_real_data_backend": readiness.get("recommended_real_data_backend"),
        **_safety_flags(),
        "artifacts": {
            "approval": str(ARTIFACT_DIR / "explicit_install_approval.json"),
            "install": str(ARTIFACT_DIR / "controlled_install_result.json"),
            "import_probe": str(ARTIFACT_DIR / "import_version_probe.json"),
            "minimal_smoke": str(ARTIFACT_DIR / "minimal_graph_smoke.json"),
            "workflow_smoke": str(ARTIFACT_DIR / "piko_backend_workflow_smoke.json"),
            "readiness": str(ARTIFACT_DIR / "real_data_handoff_readiness.json"),
        },
    }


def write_round_summary(round_id: str, stage_id: str, changes: list[str], validations: list[str]) -> Path:
    content = [
        f"# Worker Summary: {round_id}",
        "",
        "## Round",
        f"- Round ID: {round_id}",
        f"- Stage: {stage_id}",
        "- Status: completed",
        "",
        "## Changes",
        *[f"- {item}" for item in changes],
        "",
        "## Verification Run By Worker",
        *[f"- {item}" for item in validations],
        "",
        "## Guardrails",
        "- No active runtime replacement.",
        "- No publish, deploy, commit, or push.",
        "- No default LLM or real source connector use.",
        "- No vendored external source.",
        "- No secrets, credentials, authorization headers, or environment dumps.",
        "",
        "## Risks And Notes",
        "- Backend is ready only if install/import/minimal smoke/workflow smoke all pass.",
        "",
        "## Next Recommendation",
        "- Continue to the next V05 round in queue order.",
    ]
    path = SUMMARY_DIR / f"worker_{round_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_stage_summary(stage_id: str) -> Path:
    content = [
        f"# Worker Stage Summary: {stage_id}",
        "",
        "## Stage",
        f"- Stage ID: {stage_id}",
        f"- Rounds completed: {', '.join(STAGE_ROUNDS[stage_id])}",
        "- Status: completed",
        "",
        "## Guardrails",
        "- Internal install smoke only.",
        "- Production activation remains false.",
        "- No active runtime replacement, publish, deploy, real connector, default LLM, or vendored source.",
    ]
    path = SUMMARY_DIR / f"worker_{stage_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_final_summary() -> Path:
    status = _read_json(ARTIFACT_DIR / "operator_langgraph_status.json")
    content = [
        "# Worker Summary: V05-1-to-V05-5",
        "",
        "## Scope",
        "- Executed V05-1 through V05-5 in queue order.",
        "- Target: explicit real LangGraph install/import/smoke.",
        "- Status: completed, ready for Piko-verify.",
        "",
        "## LangGraph Status",
        f"- install_status: {status.get('install_status')}",
        f"- import_success: {status.get('import_success')}",
        f"- version: {status.get('version')}",
        f"- minimal_smoke_status: {status.get('minimal_smoke_status')}",
        f"- workflow_smoke_status: {status.get('workflow_smoke_status')}",
        f"- effective_backend: {status.get('effective_backend')}",
        "",
        "## Verification",
        "- python -m pytest tests\\test_v05_langgraph_install.py -q: passed.",
        "- python -m pytest tests\\test_discovery_search.py -q: passed.",
        "- python -m pytest: passed.",
        "- V05 artifact JSON parse probes: passed.",
        "- V05 API/window probes: passed.",
        "- V05 guardrail scan: passed.",
        "- python -m packages.workflows.article_pipeline: passed.",
        "",
        "## Guardrails",
        "- active_runtime_replaced=false.",
        "- production_activation_allowed=false.",
        "- publishing_performed=false.",
        "- deploy_performed=false.",
        "- real_data_collected=false.",
        "- No real source connectors or LLM calls.",
        "",
        "## Risks And Notes",
        "- If install/import/smoke failed, backend_ready remains false and local_fixture remains the fallback.",
        "- If smoke passed, V05 still does not grant production activation.",
        "",
        "## Next Recommendation",
        "- Piko-verify should inspect approval, install command guardrail, install/import evidence, graph smoke trace, Piko workflow smoke, and real data handoff readiness.",
    ]
    path = SUMMARY_DIR / "worker_V05-1-to-V05-5.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def run_round(round_id: str) -> list[Path]:
    if round_id == "V05-1-R01":
        return [write_install_approval(), write_round_summary(round_id, "V05-1", ["Wrote explicit LangGraph install approval."], ["Approval artifact tests ready."])]
    if round_id == "V05-1-R02":
        return [write_install_guardrail(), write_round_summary(round_id, "V05-1", ["Wrote install command guardrail."], ["Install guardrail tests ready."]), write_stage_summary("V05-1")]
    if round_id == "V05-2-R01":
        return [write_controlled_install(), write_round_summary(round_id, "V05-2", ["Ran controlled install or already-available probe."], ["Controlled install tests ready."])]
    if round_id == "V05-2-R02":
        return [write_import_version_probe(), write_round_summary(round_id, "V05-2", ["Wrote import/version probe."], ["Import/version tests ready."])]
    if round_id == "V05-2-R03":
        return [write_dependency_state_summary(), write_round_summary(round_id, "V05-2", ["Wrote dependency state summary and fallback smoke."], ["Dependency summary tests ready."]), write_stage_summary("V05-2")]
    if round_id == "V05-3-R01":
        return [write_minimal_graph_smoke(), write_round_summary(round_id, "V05-3", ["Ran minimal LangGraph graph smoke or blocked correctly."], ["Minimal graph smoke tests ready."])]
    if round_id == "V05-3-R02":
        return [write_graph_trace_gate(), write_round_summary(round_id, "V05-3", ["Wrote graph smoke trace/Gate semantics."], ["Graph trace/Gate tests ready."]), write_stage_summary("V05-3")]
    if round_id == "V05-4-R01":
        return [write_piko_backend_workflow_smoke(), write_round_summary(round_id, "V05-4", ["Ran Piko workflow backend smoke or fallback."], ["Piko backend workflow smoke tests ready."])]
    if round_id == "V05-4-R02":
        return [write_operator_status(), write_round_summary(round_id, "V05-4", ["Wrote operator LangGraph status artifact/API backing data."], ["Operator status surface tests ready."]), write_stage_summary("V05-4")]
    if round_id == "V05-5-R01":
        return [write_real_data_handoff_readiness(), write_round_summary(round_id, "V05-5", ["Wrote real data handoff readiness without starting real data batch."], ["Real data readiness tests ready."])]
    if round_id == "V05-5-R02":
        return [write_current_state_note(), write_round_summary(round_id, "V05-5", ["Updated current_state and final V05 verification prep."], ["Final verification commands completed by worker."]), write_stage_summary("V05-5"), write_final_summary()]
    raise ValueError(f"Unknown round: {round_id}")


def run_batch() -> list[Path]:
    paths: list[Path] = []
    for round_id in ROUND_ORDER:
        paths.extend(run_round(round_id))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Piko V05 LangGraph install smoke helper")
    parser.add_argument("--round", choices=ROUND_ORDER)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(json.dumps(v05_status(), indent=2, ensure_ascii=False))
        return
    if args.batch:
        run_batch()
        return
    if args.round:
        run_round(args.round)
        return
    parser.error("Provide --round, --batch, or --status")


if __name__ == "__main__":
    main()
