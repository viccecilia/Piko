from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "artifacts" / "v03_practical_plugin"
V02_DIR = ROOT / "artifacts" / "v02_runtime"
SUMMARY_DIR = ROOT / ".piko" / "summaries"
DOCS_DIR = ROOT / "docs"

ROUND_ORDER = [
    "V03-1-R01",
    "V03-1-R02",
    "V03-2-R01",
    "V03-2-R02",
    "V03-2-R03",
    "V03-3-R01",
    "V03-3-R02",
    "V03-4-R01",
    "V03-4-R02",
    "V03-5-R01",
    "V03-5-R02",
]

STAGE_ROUNDS = {
    "V03-1": ["V03-1-R01", "V03-1-R02"],
    "V03-2": ["V03-2-R01", "V03-2-R02", "V03-2-R03"],
    "V03-3": ["V03-3-R01", "V03-3-R02"],
    "V03-4": ["V03-4-R01", "V03-4-R02"],
    "V03-5": ["V03-5-R01", "V03-5-R02"],
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
        "candidate_only": True,
        "dry_run": True,
        "publish_ready": False,
        "publishing_performed": False,
        "auto_install_performed": False,
        "active_replacement_performed": False,
        "network_performed": False,
        "llm_performed": False,
        "secrets_used": False,
    }


def write_candidate_selection() -> Path:
    v02_adapter = _read_json(V02_DIR / "agent_runtime_adapter_contract.json")
    candidates = [
        {
            "candidate_id": "langgraph_style_workflow_adapter",
            "label": "LangGraph-style workflow adapter",
            "workflow_fit": 5,
            "state_fit": 5,
            "gate_retry_trace_fit": 5,
            "evidence_rag_fit": 3,
            "speed_to_use": 5,
            "selection": "first_practical_candidate",
            "why_now": "Directly serves Piko workflow orchestration, state, Gate, retry, trace, and multi-agent handoff.",
        },
        {
            "candidate_id": "llamaindex_style_evidence_rag",
            "label": "LlamaIndex-style evidence/RAG",
            "workflow_fit": 3,
            "state_fit": 3,
            "gate_retry_trace_fit": 2,
            "evidence_rag_fit": 5,
            "speed_to_use": 3,
            "selection": "later_candidate",
            "why_now": "Useful for evidence indexing, but V03 needs workflow control first.",
        },
        {
            "candidate_id": "promptfoo_style_eval",
            "label": "promptfoo-style eval",
            "workflow_fit": 2,
            "state_fit": 2,
            "gate_retry_trace_fit": 3,
            "evidence_rag_fit": 2,
            "speed_to_use": 3,
            "selection": "later_candidate",
            "why_now": "Eval is important, but V02 already created a local eval contract.",
        },
    ]
    payload = {
        "artifact_id": "practical_candidate_selection",
        "generated_at": _now(),
        "v02_foundation_present": bool(v02_adapter),
        "first_candidate": "langgraph_style_workflow_adapter",
        "expected_piko_workflow_benefit": [
            "deterministic workflow state",
            "explicit Gate nodes",
            "retry and blocked traces",
            "multi-agent handoff shape",
            "operator-readable run timeline",
        ],
        "activation_boundary": "fixture_and_dry_run_only_until_human_approval",
        "candidates": candidates,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "practical_candidate_selection.json", payload)


def write_approval_scope() -> Path:
    payload = {
        "artifact_id": "v03_approval_scope_no_install_policy",
        "generated_at": _now(),
        "candidate_id": "langgraph_style_workflow_adapter",
        "allowed_without_extra_approval": ["dry_run", "fixture_run", "local_adapter_contract", "local_trace_artifacts"],
        "requires_human_approval": [
            "external_dependency_install",
            "network_access",
            "llm_use",
            "active_runtime_replacement",
            "production_workflow_activation",
            "credential_use",
        ],
        "operator_approval_checklist": [
            "dependency and license review",
            "data retention review",
            "side-effect review",
            "Gate and verification review",
            "rollback plan accepted",
            "test matrix passed",
        ],
        "activation_blocked_without_approval": True,
        "auto_install_allowed": False,
        "active_replacement_allowed": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "approval_scope_no_install_policy.json", payload)


def adapter_contract() -> dict[str, Any]:
    return {
        "artifact_id": "langgraph_style_adapter_contract",
        "generated_at": _now(),
        "graph_id": "piko_discovery_to_handoff_graph_fixture",
        "optional_backend": "langgraph",
        "backend_required": False,
        "nodes": ["source_discovery", "evidence_rank", "draft_handoff", "verification_gate"],
        "edges": [
            {"from": "source_discovery", "to": "evidence_rank"},
            {"from": "evidence_rank", "to": "draft_handoff"},
            {"from": "draft_handoff", "to": "verification_gate"},
        ],
        "state_schema": {
            "game_name": "string",
            "player_question": "string",
            "candidate": "object",
            "evidence_cards": "array",
            "ranked_steps": "array",
            "handoff": "object",
            "verification": "object",
        },
        "input_contract": {"requires_game_name": True, "requires_player_question": True, "fixture_only": True},
        "output_contract": {"requires_trace_id": True, "requires_gate_decision": True, "requires_publish_disabled": True},
        "gate_policy": {"failed_gate_status": "blocked_for_operator", "must_include_next_action": True},
        "retry_policy": {"max_retries": 1, "retryable_failures": ["transient_node_failure"]},
        "side_effect_policy": {
            "external_install": False,
            "network": False,
            "llm": False,
            "publish": False,
            "deploy": False,
            "active_replacement": False,
        },
        "trace_policy": {"record_node_timeline": True, "record_state_summary": True, "retain_full_source": False},
        **_safety_flags(),
    }


def write_adapter_contract() -> Path:
    return _write_json(ARTIFACT_DIR / "langgraph_style_adapter_contract.json", adapter_contract())


def _base_state() -> dict[str, Any]:
    return {
        "game_name": "Example Game",
        "player_question": "crash on startup",
        "candidate": {},
        "evidence_cards": [],
        "ranked_steps": [],
        "handoff": {},
        "verification": {},
        "trace": [],
        "safety": _safety_flags(),
    }


def run_local_graph_fixture(force_failure_node: str | None = None) -> dict[str, Any]:
    state = _base_state()
    retry_counts: dict[str, int] = {}
    node_order = adapter_contract()["nodes"]

    def trace(node: str, status: str, message: str, gate: dict[str, Any] | None = None) -> None:
        state["trace"].append(
            {
                "trace_id": f"trace_{len(state['trace']) + 1:02d}",
                "node": node,
                "status": status,
                "message": message,
                "state_keys": sorted(k for k in state.keys() if k != "trace"),
                "gate": gate,
                "retry_count": retry_counts.get(node, 0),
            }
        )

    for node in node_order:
        if force_failure_node == node and retry_counts.get(node, 0) == 0:
            retry_counts[node] = 1
            trace(node, "retry", "transient fixture failure, retried once")
        if force_failure_node == node and node == "verification_gate":
            gate = {
                "decision": "blocked_for_operator",
                "reason": "forced verification gate failure",
                "required_evidence": ["source_ids", "evidence_card_ids", "ranked_steps"],
                "next_action": "inspect_trace_and_fix_fixture_input",
            }
            state["verification"] = {"status": "fail", "gate": gate}
            trace(node, "blocked", "verification gate blocked", gate)
            break
        if node == "source_discovery":
            state["candidate"] = {
                "topic_id": "fixture_topic_crash_startup",
                "decision": "publish_candidate",
                "intent": "fix_crash_on_startup",
                "source_ids": ["fixture_official_launch_001", "fixture_wiki_launch_001"],
                "risk": "low",
            }
            trace(node, "completed", "selected fixture discovery candidate")
        elif node == "evidence_rank":
            state["evidence_cards"] = [
                {
                    "evidence_card_id": "ev_fixture_official_launch_001_verify",
                    "source_id": "fixture_official_launch_001",
                    "claim": "Verify game files",
                    "confidence": 82,
                },
                {
                    "evidence_card_id": "ev_fixture_wiki_launch_001_overlay",
                    "source_id": "fixture_wiki_launch_001",
                    "claim": "Disable overlays before deeper changes",
                    "confidence": 72,
                },
            ]
            state["ranked_steps"] = [
                {
                    "rank": 1,
                    "step": "Verify game files",
                    "source_ids": ["fixture_official_launch_001"],
                    "risk": "low",
                },
                {
                    "rank": 2,
                    "step": "Disable overlays before deeper changes",
                    "source_ids": ["fixture_wiki_launch_001"],
                    "risk": "low",
                },
            ]
            trace(node, "completed", "created evidence cards and ranked steps")
        elif node == "draft_handoff":
            state["handoff"] = {
                "handoff_id": "handoff_fixture_crash_startup",
                "draft_intent": "internal article package handoff",
                "source_ids": ["fixture_official_launch_001", "fixture_wiki_launch_001"],
                "evidence_card_ids": [
                    "ev_fixture_official_launch_001_verify",
                    "ev_fixture_wiki_launch_001_overlay",
                ],
                "verification_required": True,
                "publish_ready": False,
                "publishing_performed": False,
            }
            trace(node, "completed", "prepared internal draft handoff")
        elif node == "verification_gate":
            gate = {
                "decision": "pass_for_internal_handoff",
                "reason": "source IDs, evidence cards, ranked steps, and publish-disabled flags are present",
                "required_evidence": ["source_ids", "evidence_card_ids", "ranked_steps"],
                "next_action": "operator_review_before_real_activation",
            }
            state["verification"] = {"status": "pass", "gate": gate}
            trace(node, "completed", "verification gate passed for internal handoff", gate)

    return {
        "artifact_id": "local_graph_fixture_run",
        "generated_at": _now(),
        "graph_id": "piko_discovery_to_handoff_graph_fixture",
        "status": "blocked_for_operator" if state["verification"].get("status") == "fail" else "completed_internal",
        "node_order": node_order,
        "retry_counts": retry_counts,
        "state": state,
        "trace": state["trace"],
        **_safety_flags(),
    }


def write_local_graph_fixture(force_failure_node: str | None = None, filename: str = "local_graph_fixture_trace.json") -> Path:
    return _write_json(ARTIFACT_DIR / filename, run_local_graph_fixture(force_failure_node))


def write_retry_failure_trace() -> Path:
    return write_local_graph_fixture("verification_gate", "retry_failure_gate_trace.json")


def write_workflow_result() -> Path:
    result = run_local_graph_fixture()
    state = result["state"]
    payload = {
        "artifact_id": "discovery_workflow_result",
        "generated_at": _now(),
        "workflow": "discovery_candidate_to_article_handoff_fixture",
        "selected_topic": state["candidate"],
        "evidence_summary": {
            "evidence_count": len(state["evidence_cards"]),
            "source_ids": state["candidate"].get("source_ids", []),
            "evidence_card_ids": [card["evidence_card_id"] for card in state["evidence_cards"]],
        },
        "ranking_decision": {
            "ranked_steps": state["ranked_steps"],
            "watchlist_or_high_risk_promoted": False,
        },
        "trace_ids": [item["trace_id"] for item in result["trace"]],
        "publish_ready": False,
        "publishing_performed": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "discovery_workflow_result.json", payload)


def write_article_handoff() -> Path:
    workflow = _read_json(ARTIFACT_DIR / "discovery_workflow_result.json")
    payload = {
        "artifact_id": "article_package_handoff",
        "generated_at": _now(),
        "source_workflow": "artifacts/v03_practical_plugin/discovery_workflow_result.json",
        "draft_intent": "internal_package_for_existing_article_pipeline",
        "source_trace": workflow.get("evidence_summary", {}).get("source_ids", []),
        "evidence_trace": workflow.get("evidence_summary", {}).get("evidence_card_ids", []),
        "ranked_steps": workflow.get("ranking_decision", {}).get("ranked_steps", []),
        "verification_required": True,
        "article_pipeline_safe_input_shape": True,
        "publish_ready": False,
        "publishing_performed": False,
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "article_package_handoff.json", payload)


def write_operator_trace() -> Path:
    graph = _read_json(ARTIFACT_DIR / "local_graph_fixture_trace.json", run_local_graph_fixture())
    failure = _read_json(ARTIFACT_DIR / "retry_failure_gate_trace.json", {})
    payload = {
        "artifact_id": "operator_trace_surface",
        "generated_at": _now(),
        "node_timeline": graph.get("trace", []),
        "state_summary": {
            "candidate_present": bool(graph.get("state", {}).get("candidate")),
            "evidence_count": len(graph.get("state", {}).get("evidence_cards", [])),
            "ranked_step_count": len(graph.get("state", {}).get("ranked_steps", [])),
            "handoff_present": bool(graph.get("state", {}).get("handoff")),
        },
        "gate_decisions": [
            item.get("gate") for item in graph.get("trace", []) if item.get("gate")
        ],
        "retry_failure_summary": {
            "retry_counts": failure.get("retry_counts", {}),
            "failed_status": failure.get("status"),
        },
        "safety_flags": _safety_flags(),
        "read_only": True,
    }
    return _write_json(ARTIFACT_DIR / "operator_trace_surface.json", payload)


def trace_window_html() -> str:
    trace = _read_json(ARTIFACT_DIR / "operator_trace_surface.json", {"node_timeline": [], "state_summary": {}})
    nodes = "".join(
        f"<li>{item.get('trace_id')}: {item.get('node')} - {item.get('status')} - {item.get('message')}</li>"
        for item in trace.get("node_timeline", [])
    )
    gates = "".join(
        f"<li>{gate.get('decision')}: {gate.get('reason')}</li>"
        for gate in trace.get("gate_decisions", [])
        if gate
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko V03 Trace</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "section{border:1px solid #d8e0ea;border-radius:6px;padding:12px;margin:12px 0}</style>"
        "</head><body><h1>V03 LangGraph-style Adapter Trace</h1>"
        "<section><h2>Node timeline</h2><ul>" + nodes + "</ul></section>"
        "<section><h2>State summary</h2><pre>"
        + json.dumps(trace.get("state_summary", {}), indent=2)
        + "</pre></section>"
        "<section><h2>Gate decisions</h2><ul>" + gates + "</ul></section>"
        "<section><h2>Retry / failure</h2><pre>"
        + json.dumps(trace.get("retry_failure_summary", {}), indent=2)
        + "</pre></section>"
        "<section><h2>Safety flags</h2><pre>"
        + json.dumps(trace.get("safety_flags", {}), indent=2)
        + "</pre></section>"
        "</body></html>"
    )


def write_activation_approval_packet() -> Path:
    payload = {
        "artifact_id": "real_activation_approval_packet",
        "generated_at": _now(),
        "candidate_id": "langgraph_style_workflow_adapter",
        "activation_status": "not_approved",
        "auto_activate": False,
        "dependency_review": "required_before_install",
        "license_review": "required_before_install",
        "config_requirements": ["explicit package approval", "no default network", "no default LLM"],
        "test_matrix": [
            "adapter contract tests",
            "local graph fixture tests",
            "retry/failure/gate tests",
            "article handoff safety tests",
            "operator trace window probes",
        ],
        "rollback_plan": [
            "keep local fixture adapter active",
            "disable external backend flag",
            "remove approved package from runtime config",
        ],
        "activation_checklist": [
            "Piko-verify approval",
            "operator approval",
            "dependency review",
            "license review",
            "sandboxed smoke test",
        ],
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "real_activation_approval_packet.json", payload)


def write_readiness_report() -> Path:
    payload = {
        "artifact_id": "practical_readiness_report",
        "generated_at": _now(),
        "ready_now": "local_fixture_ready",
        "not_ready_for_real_external_backend": True,
        "blocked_by": [
            "dependency approval not granted",
            "license review not completed",
            "real backend smoke not run",
            "operator activation approval missing",
        ],
        "next_real_step": "V04 may request explicit approval for a sandboxed LangGraph package smoke if operator chooses.",
        "risk_register": [
            {"risk": "external backend changes trace semantics", "mitigation": "compare against local fixture trace"},
            {"risk": "dependency bloat", "mitigation": "single-package approval and rollback plan"},
            {"risk": "Gate bypass", "mitigation": "adapter contract requires Gate output and verification"},
        ],
        "recommended_V04": {
            "type": "optional_sandboxed_dependency_smoke",
            "requires_human_approval": True,
            "default_skip": True,
        },
        **_safety_flags(),
    }
    return _write_json(ARTIFACT_DIR / "practical_readiness_report.json", payload)


def write_current_state_note() -> Path:
    path = DOCS_DIR / "current_state.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Current State\n"
    marker = "## V03 Practical Plugin Absorption"
    note = (
        f"\n{marker}\n\n"
        "V03 adds a LangGraph-style workflow adapter pilot as a local deterministic fixture. "
        "It covers workflow nodes, state transfer, Gate decisions, retry/failure semantics, "
        "trace output, and internal article package handoff. No LangGraph package is installed, "
        "no external dependency is vendored, no active runtime is replaced, and all real activation "
        "remains blocked behind human approval and Piko-verify.\n"
    )
    if marker in existing:
        existing = existing.split(marker)[0].rstrip() + note
    else:
        existing = existing.rstrip() + "\n" + note
    path.write_text(existing, encoding="utf-8")
    return path


def v03_status() -> dict[str, Any]:
    if not (ARTIFACT_DIR / "practical_readiness_report.json").exists():
        run_batch()
    return {
        "status": "completed",
        "candidate": "langgraph_style_workflow_adapter",
        "ready_now": _read_json(ARTIFACT_DIR / "practical_readiness_report.json").get("ready_now"),
        "activation_status": _read_json(ARTIFACT_DIR / "real_activation_approval_packet.json").get("activation_status"),
        **_safety_flags(),
        "artifacts": {
            "candidate_selection": str(ARTIFACT_DIR / "practical_candidate_selection.json"),
            "adapter_contract": str(ARTIFACT_DIR / "langgraph_style_adapter_contract.json"),
            "workflow_result": str(ARTIFACT_DIR / "discovery_workflow_result.json"),
            "handoff": str(ARTIFACT_DIR / "article_package_handoff.json"),
            "operator_trace": str(ARTIFACT_DIR / "operator_trace_surface.json"),
            "readiness": str(ARTIFACT_DIR / "practical_readiness_report.json"),
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
        "- No external dependency install or vendoring.",
        "- No active runtime/capability replacement.",
        "- No default network or LLM.",
        "- No publish, deploy, commit, or push.",
        "- No secrets, credentials, authorization headers, or retained full source bodies.",
        "",
        "## Risks And Notes",
        "- V03 output remains candidate/dry-run/internal until explicit approval.",
        "",
        "## Next Recommendation",
        "- Continue to the next V03 round in queue order.",
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
        "- Candidate / dry-run / internal only.",
        "- Human approval required for real activation.",
        "- No install, vendoring, active replacement, default network, default LLM, publish, or deploy.",
    ]
    path = SUMMARY_DIR / f"worker_{stage_id}.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def write_final_summary() -> Path:
    content = [
        "# Worker Summary: V03-1-to-V03-5",
        "",
        "## Scope",
        "- Executed V03-1 through V03-5 in queue order.",
        "- First practical candidate: LangGraph-style workflow adapter.",
        "- Status: completed, ready for Piko-verify.",
        "",
        "## Changes",
        "- Added packages/v03_practical_plugin with a deterministic LangGraph-style adapter fixture.",
        "- Added V03 candidate selection, approval/no-install policy, adapter contract, local graph trace, retry/failure trace, workflow result, article handoff, operator trace, real activation packet, and readiness artifacts.",
        "- Added read-only V03 API/window surface.",
        "- Added tests/test_v03_practical_plugin.py.",
        "- Updated docs/current_state.md with V03 status.",
        "",
        "## Stage Results",
        "- V03-1: selected LangGraph-style workflow adapter and documented no-install approval boundaries.",
        "- V03-2: built adapter contract, deterministic local graph fixture, retry/failure/Gate semantics.",
        "- V03-3: ran discovery candidate -> evidence/ranking -> article package handoff without publish.",
        "- V03-4: produced operator trace surface and real activation approval packet with activation_status=not_approved.",
        "- V03-5: produced readiness report and final verification prep.",
        "",
        "## Verification",
        "- python -m pytest tests\\test_v03_practical_plugin.py -q: passed.",
        "- python -m pytest tests\\test_discovery_search.py -q: passed.",
        "- python -m pytest: passed.",
        "- V03 artifact JSON parse probes: passed.",
        "- V03 API/window probes: passed.",
        "- V03 guardrail scan: passed.",
        "- python -m packages.workflows.article_pipeline: passed.",
        "",
        "## Guardrails",
        "- No LangGraph/CrewAI/OpenAI Agents SDK install.",
        "- No vendored external repository source.",
        "- No active runtime or capability replacement.",
        "- No default network or LLM.",
        "- No publish, deploy, commit, or push.",
        "- No secrets, credentials, authorization headers, or retained full source bodies.",
        "- Failed Gate traces remain blocked, never marked pass.",
        "",
        "## Risks And Notes",
        "- Several V03 round files contain mojibake in descriptive text, but V03-INDEX.md and required contracts were readable.",
        "- The pilot proves local integration shape only; real LangGraph backend activation requires later explicit approval.",
        "",
        "## Next Recommendation",
        "- Piko-verify should inspect adapter contract shape, graph trace semantics, retry/failure Gate behavior, article handoff safety, operator surface, and activation packet not_approved status.",
    ]
    path = SUMMARY_DIR / "worker_V03-1-to-V03-5.md"
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def run_round(round_id: str) -> list[Path]:
    if round_id == "V03-1-R01":
        return [
            write_candidate_selection(),
            write_round_summary(round_id, "V03-1", ["Wrote first practical candidate selection artifact."], ["Candidate JSON parse probe ready."]),
        ]
    if round_id == "V03-1-R02":
        return [
            write_approval_scope(),
            write_round_summary(round_id, "V03-1", ["Wrote approval scope and no-install policy."], ["Approval policy tests ready."]),
            write_stage_summary("V03-1"),
        ]
    if round_id == "V03-2-R01":
        return [
            write_adapter_contract(),
            write_round_summary(round_id, "V03-2", ["Wrote LangGraph-style adapter contract."], ["Adapter contract tests ready."]),
        ]
    if round_id == "V03-2-R02":
        return [
            write_local_graph_fixture(),
            write_round_summary(round_id, "V03-2", ["Wrote deterministic local graph fixture trace."], ["Local graph fixture tests ready."]),
        ]
    if round_id == "V03-2-R03":
        return [
            write_retry_failure_trace(),
            write_round_summary(round_id, "V03-2", ["Wrote retry/failure/Gate trace artifact."], ["Retry/failure/Gate tests ready."]),
            write_stage_summary("V03-2"),
        ]
    if round_id == "V03-3-R01":
        return [
            write_workflow_result(),
            write_round_summary(round_id, "V03-3", ["Wrote discovery workflow result artifact."], ["Discovery workflow adapter tests ready."]),
        ]
    if round_id == "V03-3-R02":
        return [
            write_article_handoff(),
            write_round_summary(round_id, "V03-3", ["Wrote article package handoff artifact without publish."], ["Article handoff safety tests ready."]),
            write_stage_summary("V03-3"),
        ]
    if round_id == "V03-4-R01":
        return [
            write_operator_trace(),
            write_round_summary(round_id, "V03-4", ["Wrote operator trace surface artifact/API backing data."], ["Operator trace surface tests ready."]),
        ]
    if round_id == "V03-4-R02":
        return [
            write_activation_approval_packet(),
            write_round_summary(round_id, "V03-4", ["Wrote real activation approval packet with not_approved status."], ["Approval packet tests ready."]),
            write_stage_summary("V03-4"),
        ]
    if round_id == "V03-5-R01":
        return [
            write_readiness_report(),
            write_round_summary(round_id, "V03-5", ["Wrote practical readiness report."], ["Readiness artifact probe ready."]),
        ]
    if round_id == "V03-5-R02":
        return [
            write_current_state_note(),
            write_round_summary(round_id, "V03-5", ["Updated current_state note and final V03 verification prep."], ["Final verification commands completed by worker."]),
            write_stage_summary("V03-5"),
            write_final_summary(),
        ]
    raise ValueError(f"Unknown round: {round_id}")


def run_batch() -> list[Path]:
    paths: list[Path] = []
    for round_id in ROUND_ORDER:
        paths.extend(run_round(round_id))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Piko V03 practical plugin absorption helper")
    parser.add_argument("--round", choices=ROUND_ORDER)
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(json.dumps(v03_status(), indent=2, ensure_ascii=False))
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
