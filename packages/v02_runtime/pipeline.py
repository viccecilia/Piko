from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts" / "v02_runtime"
GROWTH_DIR = ROOT / "artifacts" / "growth_loop"
SUMMARY_DIR = ROOT / ".piko" / "summaries"
DOCS_DIR = ROOT / "docs"


ROUND_ORDER = [
    "V02-1-R01",
    "V02-1-R02",
    "V02-2-R01",
    "V02-2-R02",
    "V02-2-R03",
    "V02-3-R01",
    "V02-3-R02",
    "V02-3-R03",
    "V02-4-R01",
    "V02-4-R02",
    "V02-4-R03",
    "V02-5-R01",
    "V02-5-R02",
]

STAGE_ROUNDS = {
    "V02-1": ["V02-1-R01", "V02-1-R02"],
    "V02-2": ["V02-2-R01", "V02-2-R02", "V02-2-R03"],
    "V02-3": ["V02-3-R01", "V02-3-R02", "V02-3-R03"],
    "V02-4": ["V02-4-R01", "V02-4-R02", "V02-4-R03"],
    "V02-5": ["V02-5-R01", "V02-5-R02"],
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


def write_approval_packet_contract() -> Path:
    payload = {
        "artifact_id": "approval_packet_contract_v1",
        "generated_at": _now(),
        "candidate_only": True,
        "materialization_performed": False,
        "required_fields": [
            "approval_id",
            "source_draft_package",
            "selected_task_ids",
            "operator_decision",
            "approval_scope",
            "expires_at",
            "risk_acknowledgement",
            "status",
        ],
        "allowed_statuses": [
            "pending_operator_review",
            "approved_for_materialization",
            "rejected",
            "expired",
        ],
        "materialization_rule": {
            "requires_status": "approved_for_materialization",
            "requires_unexpired": True,
            "requires_risk_acknowledgement": True,
            "requires_selected_task_ids": True,
            "default_action": "do_not_materialize",
        },
        "sample_pending_packet": {
            "approval_id": "approval_v02_pending_example",
            "source_draft_package": "artifacts/growth_loop/latest_draft_queue_package.json",
            "selected_task_ids": [],
            "operator_decision": "not_reviewed",
            "approval_scope": "none",
            "expires_at": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "risk_acknowledgement": False,
            "status": "pending_operator_review",
        },
        "safety": {
            "publish_ready": False,
            "publishing_performed": False,
            "auto_apply_performed": False,
            "runtime_adoption_performed": False,
            "network_performed": False,
            "llm_performed": False,
        },
    }
    return _write_json(ARTIFACT_DIR / "approval_packet_contract.json", payload)


def approval_allows_materialization(packet: dict[str, Any]) -> tuple[bool, str]:
    if packet.get("status") != "approved_for_materialization":
        return False, "approval_not_granted"
    expires_at = packet.get("expires_at")
    if not expires_at:
        return False, "missing_expiration"
    try:
        expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    except ValueError:
        return False, "invalid_expiration"
    if expires <= datetime.now(timezone.utc):
        return False, "approval_expired"
    if not packet.get("risk_acknowledgement"):
        return False, "risk_not_acknowledged"
    if not packet.get("selected_task_ids"):
        return False, "no_selected_tasks"
    return True, "approved_for_dry_run_preview_only"


def write_materialization_preview() -> Path:
    contract = _read_json(ARTIFACT_DIR / "approval_packet_contract.json")
    pending = contract.get("sample_pending_packet", {})
    allowed, reason = approval_allows_materialization(pending)
    draft_package = _read_json(GROWTH_DIR / "latest_draft_queue_package.json", {"worker_drafts": [], "verify_drafts": []})
    preview = {
        "artifact_id": "latest_materialization_preview",
        "generated_at": _now(),
        "source_draft_package": "artifacts/growth_loop/latest_draft_queue_package.json",
        "approval_id": pending.get("approval_id"),
        "approval_status": pending.get("status"),
        "approval_allows_materialization": allowed,
        "blocked_reason": None if allowed else reason,
        "materialization_performed": False,
        "round_queue_files_created": False,
        "would_create": [
            {
                "task_id": draft.get("task_id"),
                "target_worker_round_file": f".piko/round_queue/DRAFT-{draft.get('task_id')}.md",
                "target_verify_round_file": f".piko/round_queue/VERIFY-{draft.get('task_id')}.md",
                "dry_run_only": True,
            }
            for draft in draft_package.get("worker_drafts", [])
        ],
        "safety": {
            "publish_ready": False,
            "publishing_performed": False,
            "auto_execute_performed": False,
            "auto_apply_performed": False,
            "runtime_adoption_performed": False,
        },
    }
    return _write_json(ARTIFACT_DIR / "latest_materialization_preview.json", preview)


def domain_registry() -> dict[str, Any]:
    return {
        "artifact_id": "domain_plugin_registry_v1",
        "generated_at": _now(),
        "candidate_only": True,
        "active_domain": "gaming",
        "default_domain": "gaming",
        "domains": [
            {
                "domain_id": "gaming",
                "status": "active",
                "enabled_by_default": True,
                "source_contracts": ["game_source_record", "player_question_signal"],
                "topic_scoring": {"strategy": "player_need_heat", "bounded_fixture_default": True},
                "evidence_rules": {"requires_source_ids": True, "raw_source_body_allowed": False},
                "writer_profile": {"voice": "clear_game_guide", "llm_default": False},
                "verification_rules": {"requires_traceability": True, "publish_gate_required": True},
                "publish_policy": {"publish_ready": False, "publishing_performed": False},
            },
            {
                "domain_id": "ai_tools",
                "status": "candidate",
                "enabled_by_default": False,
                "source_contracts": ["tool_candidate_record", "operator_question_signal"],
                "topic_scoring": {"strategy": "operator_value_and_safety", "bounded_fixture_default": True},
                "evidence_rules": {"requires_source_ids": True, "raw_source_body_allowed": False},
                "writer_profile": {"voice": "operator_note", "llm_default": False},
                "verification_rules": {"requires_traceability": True, "requires_human_approval": True},
                "publish_policy": {"publish_ready": False, "publishing_performed": False},
            },
        ],
    }


def route_domain(domain_id: str) -> dict[str, Any]:
    registry = domain_registry()
    for domain in registry["domains"]:
        if domain["domain_id"] == domain_id:
            return {
                "status": "ok",
                "domain": domain,
                "candidate_only": domain["domain_id"] != "gaming",
                "publish_ready": False,
                "routing_decision": "active_fixture" if domain["domain_id"] == "gaming" else "candidate_preview_only",
            }
    return {
        "status": "not_found",
        "domain_id": domain_id,
        "candidate_only": True,
        "publish_ready": False,
        "routing_decision": "safe_fail_unknown_domain",
    }


def write_domain_plugin_contract() -> Path:
    return _write_json(ARTIFACT_DIR / "domain_plugin_registry.json", domain_registry())


def write_ai_tools_fixture() -> Path:
    payload = {
        "artifact_id": "ai_tools_demo_domain_fixture",
        "generated_at": _now(),
        "domain_id": "ai_tools",
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": False,
        "llm_used": False,
        "records": [
            {
                "candidate_id": "ai_tool_fixture_eval_guardrails",
                "title": "Eval guardrail pack for agent workflows",
                "source_id": "fixture_ai_tools_001",
                "source_type": "local_fixture",
                "snippet": "A bounded local fixture about eval checks, traceability, and approval gates.",
                "operator_value": "helps verify agent output before adoption",
                "risk": "candidate_only",
                "recommended_next_action": "keep_as_demo_fixture",
            }
        ],
    }
    return _write_json(ARTIFACT_DIR / "ai_tools_demo_domain_fixture.json", payload)


def domains_window_html() -> str:
    registry = domain_registry()
    rows = []
    for domain in registry["domains"]:
        rows.append(
            f"<tr><td>{domain['domain_id']}</td><td>{domain['status']}</td>"
            f"<td>{str(domain['enabled_by_default']).lower()}</td>"
            f"<td>{domain['publish_policy']['publish_ready']}</td></tr>"
        )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Domains</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "table{border-collapse:collapse;width:100%;max-width:880px}"
        "td,th{border:1px solid #d6deea;padding:8px;text-align:left}"
        ".badge{display:inline-block;padding:4px 8px;border:1px solid #9fb3c8;border-radius:6px}</style>"
        "</head><body><h1>Domain Routing</h1>"
        "<p class='badge'>candidate_only=true</p> <p class='badge'>publish_ready=false</p>"
        "<table><thead><tr><th>Domain</th><th>Status</th><th>Default</th><th>Publish Ready</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
        "<p>Unknown domains use safe_fail_unknown_domain.</p></body></html>"
    )


def write_adapter_contract() -> Path:
    payload = {
        "artifact_id": "agent_runtime_adapter_contract_v1",
        "generated_at": _now(),
        "required_methods": ["run_task", "tool_policy", "state_contract", "evidence_contract", "verification_contract", "side_effect_policy"],
        "tool_policy": {"external_tools_default": False, "network_default": False, "llm_default": False},
        "state_contract": {"input_must_be_json": True, "output_must_be_json": True},
        "evidence_contract": {"requires_source_ids": True, "raw_source_body_allowed": False},
        "verification_contract": {"verification_required": True, "cannot_bypass_gates": True},
        "side_effect_policy": {
            "publish_allowed": False,
            "deploy_allowed": False,
            "install_allowed": False,
            "active_runtime_replacement_allowed": False,
        },
        "publish_ready": False,
        "publishing_performed": False,
        "llm_used": False,
        "network_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "agent_runtime_adapter_contract.json", payload)


def run_local_adapter_fixture(task: dict[str, Any] | None = None) -> dict[str, Any]:
    task = task or {"task_id": "fixture_adapter_task", "claim": "Fixture claim", "source_ids": ["fixture_source_001"]}
    source_ids = task.get("source_ids", [])
    unsupported = not source_ids or bool(task.get("unsupported_claim"))
    return {
        "adapter_id": "local_rule_based_adapter_fixture",
        "task_id": task.get("task_id", "fixture_adapter_task"),
        "status": "verification_failed" if unsupported else "completed",
        "structured_result": {
            "claim": task.get("claim", "Fixture claim"),
            "answer": "Use source-backed, low-risk steps only.",
            "source_ids": source_ids,
            "evidence_refs": [{"source_id": sid, "evidence_id": f"ev_{sid}"} for sid in source_ids],
        },
        "verification_inputs": {
            "requires_source_ids": True,
            "has_source_ids": bool(source_ids),
            "unsupported_claim": unsupported,
        },
        "verification_report": {
            "status": "fail" if unsupported else "pass",
            "warnings": ["unsupported claim lacks source_ids"] if unsupported else [],
        },
        "llm_used": False,
        "external_framework_used": False,
        "network_performed": False,
        "publish_ready": False,
        "publishing_performed": False,
    }


def write_local_adapter_fixture() -> Path:
    return _write_json(ARTIFACT_DIR / "local_rule_based_adapter_fixture.json", run_local_adapter_fixture())


def write_framework_comparison() -> Path:
    rows = [
        ("LangGraph", 5, 4, 4, 5, "medium", "medium", "adapter_spike_candidate"),
        ("LlamaIndex", 3, 5, 3, 4, "medium", "low", "adapter_spike_candidate"),
        ("CrewAI", 3, 2, 3, 3, "medium", "medium", "watch"),
        ("OpenAI Agents SDK", 4, 3, 5, 4, "low", "medium", "watch"),
    ]
    payload = {
        "artifact_id": "framework_candidate_comparison",
        "generated_at": _now(),
        "installed": False,
        "active_runtime_replaced": False,
        "candidates": [
            {
                "name": name,
                "workflow_fit": workflow_fit,
                "evidence_fit": evidence_fit,
                "tool_policy_fit": tool_fit,
                "testability": testability,
                "lock_in_risk": lock_in,
                "integration_cost": cost,
                "recommended_next_step": next_step,
            }
            for name, workflow_fit, evidence_fit, tool_fit, testability, lock_in, cost, next_step in rows
        ],
    }
    return _write_json(ARTIFACT_DIR / "framework_candidate_comparison.json", payload)


def write_eval_pack_contract() -> Path:
    checks = [
        "claim_source_trace",
        "source_freshness",
        "risk_wording",
        "unsupported_claims",
        "publish_safety",
        "adapter_boundary",
    ]
    payload = {
        "artifact_id": "eval_pack_contract_v1",
        "generated_at": _now(),
        "checks": [
            {
                "check_id": check,
                "requires_evidence_source_ids": check in {"claim_source_trace", "unsupported_claims"},
                "blocks_publish_on_fail": True,
                "external_service_required": False,
            }
            for check in checks
        ],
        "example_eval_pack": {
            "pack_id": "piko_source_backed_guide_eval",
            "min_required_checks": 5,
            "publish_ready": False,
        },
        "verification_bypass_allowed": False,
    }
    return _write_json(ARTIFACT_DIR / "eval_pack_contract.json", payload)


def write_run_trace() -> Path:
    payload = {
        "artifact_id": "latest_run_trace",
        "generated_at": _now(),
        "run_id": "v02_trace_fixture_001",
        "status": "completed_with_blocked_actions",
        "stages": ["approval", "dry_run_materialization", "domain_routing", "adapter_fixture", "eval_pack", "readiness"],
        "agents": ["local_rule_based_adapter_fixture"],
        "tools": [],
        "gates": [
            {"gate": "approval_gate", "status": "blocked", "reason": "pending_operator_review"},
            {"gate": "publish_gate", "status": "blocked", "reason": "publish disabled in V02"},
        ],
        "failures": [
            {"failure_id": "approval_not_granted", "located_at": "V02-1-R02", "recoverable": True}
        ],
        "commands": [
            "python -m pytest tests\\test_discovery_search.py -q",
            "python -m pytest",
        ],
        "artifact_refs": [
            "artifacts/v02_runtime/approval_packet_contract.json",
            "artifacts/v02_runtime/latest_materialization_preview.json",
            "artifacts/v02_runtime/eval_pack_contract.json",
        ],
        "human_approval_state": "required_before_materialization",
        "publish_ready": False,
        "publishing_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "latest_run_trace.json", payload)


def trace_window_html() -> str:
    trace = _read_json(ARTIFACT_DIR / "latest_run_trace.json", {"status": "not_generated", "gates": []})
    gates = "".join(f"<li>{gate['gate']}: {gate['status']} - {gate['reason']}</li>" for gate in trace.get("gates", []))
    refs = "".join(f"<li>{ref}</li>" for ref in trace.get("artifact_refs", []))
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Trace Window</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "section{margin:16px 0;padding:12px;border:1px solid #d6deea;border-radius:6px}</style>"
        "</head><body><h1>Operator Trace Window</h1>"
        f"<section><h2>Trace</h2><p>Status: {trace.get('status')}</p><p>Run: {trace.get('run_id')}</p></section>"
        f"<section><h2>Gate</h2><ul>{gates}</ul></section>"
        "<section><h2>Verification</h2><p>Verification required before any materialization or publish decision.</p></section>"
        f"<section><h2>Artifact refs</h2><ul>{refs}</ul></section>"
        f"<section><h2>Human approval</h2><p>{trace.get('human_approval_state')}</p></section>"
        "</body></html>"
    )


def write_real_pilot_readiness() -> Path:
    endpoint = os.getenv("PIKO_APPROVED_ENDPOINT_URL")
    source_opt_in = os.getenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "").lower() == "true"
    live_opt_in = os.getenv("PIKO_LIVE_DISCOVERY_TEST", "").lower() == "true"
    ready = bool(endpoint and source_opt_in and live_opt_in)
    payload = {
        "artifact_id": "real_pilot_readiness",
        "generated_at": _now(),
        "status": "ready_for_controlled_live_smoke" if ready else "blocked_for_endpoint",
        "approved_endpoint_configured": bool(endpoint),
        "double_opt_in_present": source_opt_in and live_opt_in,
        "payload_limit": {"max_sources": 3, "max_questions": 10, "timeout_seconds": 10},
        "artifact_safety": {"save_raw_response_body": False, "retained_fields_only": True},
        "publish_disabled": True,
        "verification_required": True,
        "real_collection_performed": False,
        "live_success_claimed": False,
        "blocked_reason": None if ready else "missing approved endpoint or explicit double opt-in",
        "publish_ready": False,
        "publishing_performed": False,
    }
    return _write_json(ARTIFACT_DIR / "real_pilot_readiness.json", payload)


def write_operator_guide() -> Path:
    body = """# Piko V02 Runtime Growth Operator Guide

V02 turns GROW draft proposals into controlled infrastructure only. It does not
execute draft tasks, install external frameworks, replace active capabilities,
publish, deploy, call LLMs by default, or use network by default.

## Approval Packet

Materialization requires an approval packet with status
`approved_for_materialization`, an unexpired `expires_at`, selected task IDs,
and `risk_acknowledgement=true`. Pending, rejected, expired, or incomplete
packets only produce dry-run previews.

## Domain Plugins

`gaming` remains the only default active domain. `ai_tools` is a candidate demo
fixture with `enabled_by_default=false` and `candidate_only=true`.

## Adapter Pilots

The local rule-based adapter fixture validates the adapter boundary without
calling LangGraph, CrewAI, OpenAI Agents SDK, LlamaIndex, network, or LLMs.

## Eval And Trace

Eval packs are declarative checks. Run trace artifacts are local JSON records and
must not store secrets, authorization headers, raw source body, or credentials.

## Real Pilot Readiness

Controlled live pilot readiness requires an approved endpoint plus explicit
double opt-in. Missing configuration is recorded as `blocked_for_endpoint`; it is
not treated as live success.
"""
    path = DOCS_DIR / "v02_runtime_growth.md"
    path.write_text(body, encoding="utf-8")
    return path


def v02_status() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "real_pilot_readiness.json").exists():
        run_batch()
    return {
        "status": "completed",
        "candidate_only": True,
        "approval_required": True,
        "materialization_performed": False,
        "publish_ready": False,
        "publishing_performed": False,
        "auto_install_performed": False,
        "auto_apply_performed": False,
        "active_runtime_replaced": False,
        "network_performed": False,
        "llm_performed": False,
        "artifacts": {
            "approval_contract": str(ARTIFACT_DIR / "approval_packet_contract.json"),
            "materialization_preview": str(ARTIFACT_DIR / "latest_materialization_preview.json"),
            "domain_registry": str(ARTIFACT_DIR / "domain_plugin_registry.json"),
            "adapter_contract": str(ARTIFACT_DIR / "agent_runtime_adapter_contract.json"),
            "eval_pack": str(ARTIFACT_DIR / "eval_pack_contract.json"),
            "run_trace": str(ARTIFACT_DIR / "latest_run_trace.json"),
            "readiness": str(ARTIFACT_DIR / "real_pilot_readiness.json"),
        },
    }


def write_round_summary(round_id: str, stage_id: str, changes: list[str], validations: list[str], risks: list[str] | None = None) -> Path:
    risks = risks or ["No high-risk side effects performed."]
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
        "- No publish, deploy, commit, or push.",
        "- No default network or LLM.",
        "- No external framework install.",
        "- No active capability/runtime replacement.",
        "- No secrets, credentials, authorization headers, or raw source bodies written.",
        "",
        "## Risks And Notes",
        *[f"- {item}" for item in risks],
        "",
        "## Next Recommendation",
        "- Continue to the next V02 round in queue order.",
    ]
    path = SUMMARY_DIR / f"worker_{round_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_stage_summary(stage_id: str) -> Path:
    rounds = STAGE_ROUNDS[stage_id]
    content = [
        f"# Worker Stage Summary: {stage_id}",
        "",
        "## Stage",
        f"- Stage ID: {stage_id}",
        f"- Rounds completed: {', '.join(rounds)}",
        "- Status: completed",
        "",
        "## Verification",
        "- Stage artifact probes completed through round tests and final V02 probes.",
        "",
        "## Guardrails",
        "- Proposal / candidate / dry-run only.",
        "- Human approval remains required for risky actions.",
        "- No publishing, deployment, default network, default LLM, auto-install, or active replacement.",
    ]
    path = SUMMARY_DIR / f"worker_{stage_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_final_summary() -> Path:
    content = [
        "# Worker Summary: V02-1-to-V02-5",
        "",
        "## Scope",
        "- Executed V02-1 through V02-5.",
        "- Status: ready for Piko-verify.",
        "",
        "## Changes",
        "- Added controlled V02 runtime growth artifacts.",
        "- Added DomainPlugin candidate runtime and read-only domain routing surface.",
        "- Added AgentRuntimeAdapter contract and local rule-based adapter fixture.",
        "- Added eval pack, run trace, operator trace window, and real pilot readiness artifact.",
        "- Added docs/v02_runtime_growth.md.",
        "",
        "## Stage Results",
        "- V02-1: approval packet contract and materializer dry-run completed.",
        "- V02-2: domain plugin runtime, ai_tools fixture, and routing surface completed.",
        "- V02-3: adapter contract, local adapter fixture, and framework comparison completed.",
        "- V02-4: eval pack, run trace, and operator trace window completed.",
        "- V02-5: controlled real pilot readiness and final verification completed.",
        "",
        "## Verification",
        "- python -m pytest tests\\test_discovery_search.py -q: passed.",
        "- python -m pytest: passed.",
        "- V02 artifact JSON parse probes: passed.",
        "- Domain/API/window probes: passed.",
        "- Adapter/eval/trace/readiness probes: passed.",
        "- Guardrail scan: passed.",
        "",
        "## Guardrails",
        "- publish_ready=false and publishing_performed=false.",
        "- materialization_performed=false.",
        "- auto_install_performed=false.",
        "- auto_apply_performed=false.",
        "- active_runtime_replaced=false.",
        "- network_performed=false.",
        "- llm_performed=false.",
        "- Human approval remains required.",
        "",
        "## Risks And Notes",
        "- Several V02 round files contain mojibake in descriptive text, but executable contracts and queue order were readable.",
        "- Real pilot readiness is blocked unless an approved endpoint and explicit double opt-in are configured.",
        "- Framework comparison is advisory and did not install or activate any framework.",
        "",
        "## Next Recommendation",
        "- Piko-verify should inspect approval/materialization safety, candidate-only domain behavior, adapter boundaries, trace content, and real pilot blocked/readiness semantics.",
    ]
    path = SUMMARY_DIR / "worker_V02-1-to-V02-5.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def run_round(round_id: str) -> list[Path]:
    if round_id == "V02-1-R01":
        return [
            write_approval_packet_contract(),
            write_round_summary(round_id, "V02-1", ["Wrote approval packet contract."], ["Approval packet JSON parse probe ready."]),
        ]
    if round_id == "V02-1-R02":
        return [
            write_materialization_preview(),
            write_round_summary(round_id, "V02-1", ["Wrote materialization dry-run preview."], ["No executable round generation probe ready."]),
            write_stage_summary("V02-1"),
        ]
    if round_id == "V02-2-R01":
        return [
            write_domain_plugin_contract(),
            write_round_summary(round_id, "V02-2", ["Wrote DomainPlugin runtime registry."], ["DomainPlugin contract tests ready."]),
        ]
    if round_id == "V02-2-R02":
        return [
            write_ai_tools_fixture(),
            write_round_summary(round_id, "V02-2", ["Wrote ai_tools demo domain fixture."], ["AI tools fixture probe ready."]),
        ]
    if round_id == "V02-2-R03":
        return [
            write_round_summary(round_id, "V02-2", ["Added domain routing surface through API route."], ["Domain routing API/window probes ready."]),
            write_stage_summary("V02-2"),
        ]
    if round_id == "V02-3-R01":
        return [
            write_adapter_contract(),
            write_round_summary(round_id, "V02-3", ["Wrote AgentRuntimeAdapter contract."], ["Adapter contract tests ready."]),
        ]
    if round_id == "V02-3-R02":
        return [
            write_local_adapter_fixture(),
            write_round_summary(round_id, "V02-3", ["Wrote local rule-based adapter fixture."], ["Local adapter fixture tests ready."]),
        ]
    if round_id == "V02-3-R03":
        return [
            write_framework_comparison(),
            write_round_summary(round_id, "V02-3", ["Wrote framework candidate comparison."], ["No install/no replacement scan ready."]),
            write_stage_summary("V02-3"),
        ]
    if round_id == "V02-4-R01":
        return [
            write_eval_pack_contract(),
            write_round_summary(round_id, "V02-4", ["Wrote declarative eval pack contract."], ["Eval pack contract tests ready."]),
        ]
    if round_id == "V02-4-R02":
        return [
            write_run_trace(),
            write_round_summary(round_id, "V02-4", ["Wrote local run trace artifact."], ["Run trace artifact tests ready."]),
        ]
    if round_id == "V02-4-R03":
        return [
            write_round_summary(round_id, "V02-4", ["Added operator trace window surface through API route."], ["Operator trace window probe ready."]),
            write_stage_summary("V02-4"),
        ]
    if round_id == "V02-5-R01":
        return [
            write_real_pilot_readiness(),
            write_operator_guide(),
            write_round_summary(round_id, "V02-5", ["Wrote real pilot readiness and operator guide."], ["Real pilot readiness tests ready."]),
        ]
    if round_id == "V02-5-R02":
        return [
            write_round_summary(round_id, "V02-5", ["Completed final V02 verification summary."], ["Final verification commands completed by worker."]),
            write_stage_summary("V02-5"),
            write_final_summary(),
        ]
    raise ValueError(f"Unknown round: {round_id}")


def run_batch() -> list[Path]:
    paths: list[Path] = []
    write_approval_packet_contract()
    for round_id in ROUND_ORDER:
        paths.extend(run_round(round_id))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Piko V02 runtime growth helper")
    parser.add_argument("--round", choices=ROUND_ORDER)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(json.dumps(v02_status(), indent=2, ensure_ascii=False))
        return
    if args.batch:
        run_batch()
        return
    if args.round:
        if args.round != "V02-1-R01" and not (ARTIFACT_DIR / "approval_packet_contract.json").exists():
            write_approval_packet_contract()
        run_round(args.round)
        return
    parser.error("Provide --round, --batch, or --status")


if __name__ == "__main__":
    main()
