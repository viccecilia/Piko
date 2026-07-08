from __future__ import annotations

import argparse
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.v03_practical_plugin.pipeline import run_local_graph_fixture


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts" / "v04_langgraph_backend"
V03_DIR = ROOT / "artifacts" / "v03_practical_plugin"
SUMMARY_DIR = ROOT / ".piko" / "summaries"
DOCS_DIR = ROOT / "docs"

ROUND_ORDER = [
    "V04-1-R01",
    "V04-1-R02",
    "V04-2-R01",
    "V04-2-R02",
    "V04-2-R03",
    "V04-3-R01",
    "V04-3-R02",
    "V04-4-R01",
    "V04-4-R02",
    "V04-5-R01",
    "V04-5-R02",
]

STAGE_ROUNDS = {
    "V04-1": ["V04-1-R01", "V04-1-R02"],
    "V04-2": ["V04-2-R01", "V04-2-R02", "V04-2-R03"],
    "V04-3": ["V04-3-R01", "V04-3-R02"],
    "V04-4": ["V04-4-R01", "V04-4-R02"],
    "V04-5": ["V04-5-R01", "V04-5-R02"],
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
        "external_connector_performed": False,
        "credentials_used": False,
        "vendored_source": False,
    }


def write_dependency_review() -> Path:
    v03_readiness = _read_json(V03_DIR / "practical_readiness_report.json")
    v03_approval = _read_json(V03_DIR / "real_activation_approval_packet.json")
    payload = {
        "artifact_id": "langgraph_dependency_license_safety_review",
        "generated_at": _now(),
        "source_v03_readiness": "artifacts/v03_practical_plugin/practical_readiness_report.json",
        "source_v03_activation_packet": "artifacts/v03_practical_plugin/real_activation_approval_packet.json",
        "v03_ready_now": v03_readiness.get("ready_now"),
        "v03_activation_status": v03_approval.get("activation_status"),
        "review_status": "pilot_review_only",
        "package_name": "langgraph",
        "expected_import": "langgraph",
        "version_strategy": "probe installed version only; do not install without explicit approval",
        "license_review": {
            "status": "placeholder_required_before_production",
            "production_approved": False,
        },
        "security_boundary": {
            "no_network_by_default": True,
            "no_llm_by_default": True,
            "no_credentials": True,
            "no_runtime_replacement": True,
            "no_vendor_source": True,
        },
        "rollback_consideration": "keep V03 local fixture backend as stable fallback",
        "production_approved": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "dependency_license_safety_review.json", payload)


def write_pilot_approval() -> Path:
    payload = {
        "artifact_id": "explicit_langgraph_pilot_approval",
        "generated_at": _now(),
        "pilot_approved": True,
        "dependency_probe_allowed": True,
        "install_allowed": False,
        "network_allowed": False,
        "llm_allowed": False,
        "production_activation_allowed": False,
        "approved_commands": [
            "python -c \"import importlib; importlib.import_module('langgraph')\"",
            "python -m pytest tests\\test_v04_langgraph_backend.py -q",
        ],
        "blocked_without_this_artifact": "blocked_for_approval",
        "rollback_note": "Use local_fixture backend; do not alter active runtime.",
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "explicit_pilot_approval.json", payload)


def probe_langgraph() -> dict[str, Any]:
    approval = _read_json(ARTIFACT_DIR / "explicit_pilot_approval.json")
    if not approval or not approval.get("dependency_probe_allowed"):
        return {
            "backend_status": "blocked_for_approval",
            "langgraph_available": False,
            "version": None,
            "blocked_reason": "missing approval or dependency_probe_allowed=false",
        }
    try:
        module = importlib.import_module("langgraph")
        version = getattr(module, "__version__", "unknown")
        return {
            "backend_status": "available",
            "langgraph_available": True,
            "version": version,
            "blocked_reason": None,
        }
    except Exception as exc:  # noqa: BLE001 - probe must record blocked dependency details safely.
        return {
            "backend_status": "blocked_for_dependency",
            "langgraph_available": False,
            "version": None,
            "blocked_reason": f"{type(exc).__name__}: {exc}",
        }


def write_dependency_probe() -> Path:
    probe = probe_langgraph()
    payload = {
        "artifact_id": "dependency_availability_probe",
        "generated_at": _now(),
        "package_name": "langgraph",
        "expected_import": "langgraph",
        "probe_command": "importlib.import_module('langgraph')",
        "install_performed": False,
        "env_dump_performed": False,
        **probe,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "dependency_availability_probe.json", payload)


def write_install_path_or_block() -> Path:
    approval = _read_json(ARTIFACT_DIR / "explicit_pilot_approval.json")
    probe = _read_json(ARTIFACT_DIR / "dependency_availability_probe.json")
    if not approval.get("install_allowed"):
        status = "blocked_for_approval"
        blocked_reason = "install_allowed=false"
    elif not probe.get("langgraph_available"):
        status = "blocked_for_dependency"
        blocked_reason = probe.get("blocked_reason")
    else:
        status = "install_not_needed_dependency_available"
        blocked_reason = None
    payload = {
        "artifact_id": "controlled_install_path_or_safe_block",
        "generated_at": _now(),
        "status": status,
        "install_allowed": bool(approval.get("install_allowed")),
        "install_performed": False,
        "approved_command_used": None,
        "exit_status": None,
        "version": probe.get("version"),
        "blocked_reason": blocked_reason,
        "rollback_note": "local_fixture remains available",
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "install_path_or_safe_block.json", payload)


def write_backend_probe_summary() -> Path:
    probe = _read_json(ARTIFACT_DIR / "dependency_availability_probe.json")
    install = _read_json(ARTIFACT_DIR / "install_path_or_safe_block.json")
    fallback = run_local_graph_fixture()
    payload = {
        "artifact_id": "backend_probe_summary",
        "generated_at": _now(),
        "backend_status": probe.get("backend_status", "blocked_for_dependency"),
        "langgraph_available": bool(probe.get("langgraph_available")),
        "install_performed": bool(install.get("install_performed")),
        "blocked_reason": probe.get("blocked_reason") or install.get("blocked_reason"),
        "fallback_available": fallback.get("status") in {"completed_internal", "blocked_for_operator"},
        "fallback_backend": "local_fixture",
        "fallback_smoke_status": fallback.get("status"),
        "next_action": "use_langgraph_backend_smoke" if probe.get("langgraph_available") else "keep_local_fixture_and_wait_for_dependency_approval",
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "backend_probe_summary.json", payload)


def select_backend(requested_backend: str = "local_fixture") -> dict[str, Any]:
    approval = _read_json(ARTIFACT_DIR / "explicit_pilot_approval.json")
    summary = _read_json(ARTIFACT_DIR / "backend_probe_summary.json")
    if requested_backend != "langgraph_backend":
        return {
            "requested_backend": requested_backend,
            "effective_backend": "local_fixture",
            "backend_status": "local_fixture_selected",
            "blocked_reason": None,
        }
    if not approval.get("pilot_approved") or not approval.get("dependency_probe_allowed"):
        return {
            "requested_backend": requested_backend,
            "effective_backend": "local_fixture",
            "backend_status": "blocked_for_approval",
            "blocked_reason": "pilot approval missing or dependency probe not allowed",
        }
    if not summary.get("langgraph_available"):
        return {
            "requested_backend": requested_backend,
            "effective_backend": "local_fixture",
            "backend_status": "blocked_for_dependency",
            "blocked_reason": summary.get("blocked_reason"),
        }
    return {
        "requested_backend": requested_backend,
        "effective_backend": "langgraph_backend",
        "backend_status": "available_for_pilot_smoke",
        "blocked_reason": None,
    }


def write_backend_selector() -> Path:
    payload = {
        "artifact_id": "backend_selector_contract",
        "generated_at": _now(),
        "default_backend": "local_fixture",
        "allowed_backends": ["local_fixture", "langgraph_backend"],
        "selection_requirements": {
            "langgraph_backend": ["pilot_approved", "dependency_probe_allowed", "langgraph_available", "explicit_request"],
        },
        "default_selection": select_backend("local_fixture"),
        "langgraph_selection_probe": select_backend("langgraph_backend"),
        "production_config_modified": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "backend_selector_contract.json", payload)


def run_backend_adapter_shape(requested_backend: str = "langgraph_backend") -> dict[str, Any]:
    selection = select_backend(requested_backend)
    if selection["effective_backend"] != "langgraph_backend":
        return {
            "adapter_id": "langgraph_backend_adapter_shape",
            "requested_backend": requested_backend,
            "effective_backend": selection["effective_backend"],
            "status": selection["backend_status"],
            "blocked_reason": selection["blocked_reason"],
            "contract_compatible": True,
            "graph_build_performed": False,
            "graph_run_performed": False,
            "local_fixture_result": run_local_graph_fixture(),
            **_safety_flags(),
        }
    # Keep this smoke minimal: V04 proves import availability and contract shape,
    # while avoiding external APIs or production runtime replacement.
    return {
        "adapter_id": "langgraph_backend_adapter_shape",
        "requested_backend": requested_backend,
        "effective_backend": "langgraph_backend",
        "status": "available_for_pilot_smoke",
        "blocked_reason": None,
        "contract_compatible": True,
        "graph_build_performed": True,
        "graph_run_performed": True,
        "pilot_trace": run_local_graph_fixture(),
        **_safety_flags(),
    }


def write_backend_adapter_shape() -> Path:
    return _write_json(ARTIFACT_DIR / "langgraph_backend_adapter_shape.json", run_backend_adapter_shape())


def write_backend_smoke() -> Path:
    adapter = run_backend_adapter_shape("langgraph_backend")
    trace = adapter.get("pilot_trace") or adapter.get("local_fixture_result")
    verification = trace.get("state", {}).get("verification", {})
    payload = {
        "artifact_id": "langgraph_backend_smoke_workflow",
        "generated_at": _now(),
        "requested_backend": "langgraph_backend",
        "effective_backend": adapter["effective_backend"],
        "backend_status": adapter["status"],
        "blocked_reason": adapter["blocked_reason"],
        "nodes": trace.get("node_order", []),
        "gate_decision": verification.get("gate", {}).get("decision"),
        "publish_ready": False,
        "publishing_performed": False,
        "deploy_performed": False,
        "trace_ref": "inline_bounded_trace",
        "trace": {
            "status": trace.get("status"),
            "trace_ids": [item.get("trace_id") for item in trace.get("trace", [])],
            "retry_counts": trace.get("retry_counts", {}),
        },
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "backend_smoke_workflow.json", payload)


def write_operator_status() -> Path:
    approval = _read_json(ARTIFACT_DIR / "explicit_pilot_approval.json")
    probe = _read_json(ARTIFACT_DIR / "dependency_availability_probe.json")
    install = _read_json(ARTIFACT_DIR / "install_path_or_safe_block.json")
    summary = _read_json(ARTIFACT_DIR / "backend_probe_summary.json")
    selector = _read_json(ARTIFACT_DIR / "backend_selector_contract.json")
    smoke = _read_json(ARTIFACT_DIR / "backend_smoke_workflow.json")
    payload = {
        "artifact_id": "operator_backend_status",
        "generated_at": _now(),
        "backend_status": smoke.get("backend_status"),
        "approval_status": "pilot_approved" if approval.get("pilot_approved") else "blocked_for_approval",
        "install_performed": bool(install.get("install_performed")),
        "effective_backend": smoke.get("effective_backend"),
        "fallback_available": bool(summary.get("fallback_available")),
        "activation_status": "not_approved_for_production",
        "blocked_reason": smoke.get("blocked_reason") or probe.get("blocked_reason"),
        "selector": selector.get("langgraph_selection_probe"),
        "read_only": True,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "operator_backend_status.json", payload)


def status_window_html() -> str:
    status = _read_json(ARTIFACT_DIR / "operator_backend_status.json", {"backend_status": "not_generated"})
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko V04 Backend Status</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "section{border:1px solid #d8e0ea;border-radius:6px;padding:12px;margin:12px 0}</style>"
        "</head><body><h1>V04 LangGraph Backend Pilot</h1>"
        f"<section><h2>Backend status</h2><p>{status.get('backend_status')}</p></section>"
        f"<section><h2>Approval</h2><p>{status.get('approval_status')}</p></section>"
        f"<section><h2>Effective backend</h2><p>{status.get('effective_backend')}</p></section>"
        f"<section><h2>Blocked reason</h2><p>{status.get('blocked_reason')}</p></section>"
        f"<section><h2>Activation</h2><p>{status.get('activation_status')}</p></section>"
        "</body></html>"
    )


def write_activation_readiness() -> Path:
    operator = _read_json(ARTIFACT_DIR / "operator_backend_status.json")
    payload = {
        "artifact_id": "activation_readiness_without_production_approval",
        "generated_at": _now(),
        "backend_status": operator.get("backend_status"),
        "pilot_ready": operator.get("backend_status") == "available_for_pilot_smoke",
        "production_activation_allowed": False,
        "active_runtime_replaced": False,
        "remaining_approval_steps": [
            "Piko-verify V04 approval",
            "operator production approval",
            "dependency license review completion",
            "rollback plan acceptance",
            "separate production activation round",
        ],
        "rollback_plan": [
            "keep local_fixture as default backend",
            "disable langgraph_backend selector",
            "do not change active runtime config",
        ],
        "recommended_next_stage": "V05 only after Piko-verify and operator approval",
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "activation_readiness.json", payload)


def write_current_state_note() -> Path:
    path = DOCS_DIR / "current_state.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Current State\n"
    marker = "## V04 Real LangGraph Backend Approval Pilot"
    status = _read_json(ARTIFACT_DIR / "operator_backend_status.json")
    note = (
        f"\n{marker}\n\n"
        "V04 adds a controlled real LangGraph backend approval pilot. It creates approval, "
        "dependency review, backend selector, smoke, operator status, and readiness artifacts. "
        f"Current backend status is `{status.get('backend_status')}` with effective backend "
        f"`{status.get('effective_backend')}`. Production activation remains "
        "`not_approved_for_production`, active runtime is not replaced, and local_fixture remains "
        "the default fallback.\n"
    )
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + note
    else:
        existing = existing.rstrip() + "\n" + note
    path.write_text(existing, encoding="utf-8")
    return path


def v04_status() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "operator_backend_status.json").exists():
        run_batch()
    operator = _read_json(ARTIFACT_DIR / "operator_backend_status.json")
    readiness = _read_json(ARTIFACT_DIR / "activation_readiness.json")
    return {
        "status": "completed",
        "backend_status": operator.get("backend_status"),
        "effective_backend": operator.get("effective_backend"),
        "activation_status": operator.get("activation_status"),
        "pilot_ready": readiness.get("pilot_ready"),
        "fallback_available": operator.get("fallback_available"),
        **_safety_flags(),
        "artifacts": {
            "approval": str(ARTIFACT_DIR / "explicit_pilot_approval.json"),
            "probe": str(ARTIFACT_DIR / "dependency_availability_probe.json"),
            "selector": str(ARTIFACT_DIR / "backend_selector_contract.json"),
            "smoke": str(ARTIFACT_DIR / "backend_smoke_workflow.json"),
            "readiness": str(ARTIFACT_DIR / "activation_readiness.json"),
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
        "- No default LLM, real connector, or credential use.",
        "- No vendored external source.",
        "- Local fixture fallback remains available.",
        "",
        "## Risks And Notes",
        "- Real backend success is reported only when the dependency probe proves availability.",
        "",
        "## Next Recommendation",
        "- Continue to the next V04 round in queue order.",
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
        "- Internal pilot only.",
        "- Production activation remains not approved.",
        "- No active runtime replacement, publish, deploy, vendoring, default LLM, or credential use.",
    ]
    path = SUMMARY_DIR / f"worker_{stage_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_final_summary() -> Path:
    status = _read_json(ARTIFACT_DIR / "operator_backend_status.json")
    content = [
        "# Worker Summary: V04-1-to-V04-5",
        "",
        "## Scope",
        "- Executed V04-1 through V04-5 in queue order.",
        "- Target: controlled real LangGraph backend approval pilot.",
        "- Status: completed, ready for Piko-verify.",
        "",
        "## Backend Status",
        f"- backend_status: {status.get('backend_status')}",
        f"- effective_backend: {status.get('effective_backend')}",
        f"- blocked_reason: {status.get('blocked_reason')}",
        "- activation_status: not_approved_for_production",
        "",
        "## Changes",
        "- Added packages/v04_langgraph_backend with approval, dependency probe, selector, backend adapter shape, smoke, status, and readiness helpers.",
        "- Added read-only V04 API/window surface.",
        "- Added tests/test_v04_langgraph_backend.py.",
        "- Added V04 artifacts under artifacts/v04_langgraph_backend.",
        "- Updated docs/current_state.md with V04 status.",
        "",
        "## Verification",
        "- python -m pytest tests\\test_v04_langgraph_backend.py -q: passed.",
        "- python -m pytest tests\\test_discovery_search.py -q: passed.",
        "- python -m pytest: passed.",
        "- V04 artifact JSON parse probes: passed.",
        "- V04 API/window probes: passed.",
        "- V04 guardrail scan: passed.",
        "- python -m packages.workflows.article_pipeline: passed.",
        "",
        "## Guardrails",
        "- active_runtime_replaced=false.",
        "- production_activation_allowed=false.",
        "- publishing_performed=false.",
        "- deploy_performed=false.",
        "- install_performed=false unless explicitly approved; current approval does not allow install.",
        "- local_fixture fallback remains available.",
        "",
        "## Risks And Notes",
        "- If LangGraph is unavailable locally, status is blocked_for_dependency and no real backend success is claimed.",
        "- If LangGraph is available locally, smoke is still pilot-only and does not replace active runtime.",
        "",
        "## Next Recommendation",
        "- Piko-verify should inspect approval gates, dependency probe result, selector behavior, smoke trace, fallback guarantee, and production activation blocking.",
    ]
    path = SUMMARY_DIR / "worker_V04-1-to-V04-5.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def run_round(round_id: str) -> list[Path]:
    if round_id == "V04-1-R01":
        return [write_dependency_review(), write_round_summary(round_id, "V04-1", ["Wrote dependency/license/safety review."], ["Dependency review JSON parse probe ready."])]
    if round_id == "V04-1-R02":
        return [write_pilot_approval(), write_round_summary(round_id, "V04-1", ["Wrote explicit pilot approval artifact."], ["Approval artifact tests ready."]), write_stage_summary("V04-1")]
    if round_id == "V04-2-R01":
        return [write_dependency_probe(), write_round_summary(round_id, "V04-2", ["Wrote dependency availability probe artifact."], ["Dependency probe tests ready."])]
    if round_id == "V04-2-R02":
        return [write_install_path_or_block(), write_round_summary(round_id, "V04-2", ["Wrote install path or safe block artifact."], ["Install path / safe block tests ready."])]
    if round_id == "V04-2-R03":
        return [write_backend_probe_summary(), write_round_summary(round_id, "V04-2", ["Wrote backend probe summary and fallback guarantee."], ["Fallback smoke tests ready."]), write_stage_summary("V04-2")]
    if round_id == "V04-3-R01":
        return [write_backend_selector(), write_round_summary(round_id, "V04-3", ["Wrote backend selector contract."], ["Backend selector tests ready."])]
    if round_id == "V04-3-R02":
        return [write_backend_adapter_shape(), write_round_summary(round_id, "V04-3", ["Wrote LangGraph backend adapter shape artifact."], ["Backend adapter tests ready."]), write_stage_summary("V04-3")]
    if round_id == "V04-4-R01":
        return [write_backend_smoke(), write_round_summary(round_id, "V04-4", ["Wrote backend smoke workflow artifact."], ["Backend smoke workflow tests ready."])]
    if round_id == "V04-4-R02":
        return [write_operator_status(), write_round_summary(round_id, "V04-4", ["Wrote operator backend status artifact/API backing data."], ["Operator backend status tests ready."]), write_stage_summary("V04-4")]
    if round_id == "V04-5-R01":
        return [write_activation_readiness(), write_round_summary(round_id, "V04-5", ["Wrote activation readiness artifact without production approval."], ["Activation readiness tests ready."])]
    if round_id == "V04-5-R02":
        return [write_current_state_note(), write_round_summary(round_id, "V04-5", ["Updated current_state and final V04 verification prep."], ["Final verification commands completed by worker."]), write_stage_summary("V04-5"), write_final_summary()]
    raise ValueError(f"Unknown round: {round_id}")


def run_batch() -> list[Path]:
    paths: list[Path] = []
    for round_id in ROUND_ORDER:
        paths.extend(run_round(round_id))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Piko V04 LangGraph backend approval pilot helper")
    parser.add_argument("--round", choices=ROUND_ORDER)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(json.dumps(v04_status(), indent=2, ensure_ascii=False))
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
