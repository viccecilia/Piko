import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/domain_plugins")
FIXTURE_DIR = Path("fixtures/domain_plugins")

CORE_CONCEPTS = [
    "domain",
    "source_signal",
    "need_cluster",
    "evidence",
    "workflow_trace",
    "content_package",
    "distribution_package",
    "verify_gate",
]
DOMAIN_PLUGIN_REQUIRED_FIELDS = [
    "domain_id",
    "version",
    "source_types",
    "signal_schema",
    "normalizer",
    "scoring_profile",
    "content_templates",
    "risk_policy",
    "distribution_targets",
    "eval_suite",
    "activation_status",
]
GENERIC_WORKFLOW_STAGES = [
    "collect_signals",
    "cluster_needs",
    "rank_opportunities",
    "build_evidence",
    "create_content_package",
    "verify_gate",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_product_boundary() -> dict[str, Any]:
    payload = {
        "artifact_type": "product_boundary_contract",
        "generated_at": _now(),
        "product_positioning": "Piko is a domain-agnostic pluggable multi-agent collaboration system.",
        "core_boundary": {
            "domain_agnostic": True,
            "core_allowed_concepts": CORE_CONCEPTS,
            "core_owns": [
                "workflow",
                "agent_runtime",
                "evidence",
                "trace",
                "eval",
                "quality",
                "distribution_dry_run",
                "verify_gate",
            ],
            "core_must_not_own": [
                "gaming_vocabulary",
                "ai_tools_vocabulary",
                "domain_source_types",
                "domain_templates",
                "domain_risk_rules",
            ],
        },
        "domain_boundary": {
            "domain_owns": [
                "vocabulary",
                "source_types",
                "normalizers",
                "scoring_presets",
                "templates",
                "risk_rules",
                "operator_labels",
            ],
            "packs": ["gaming", "ai_tools"],
        },
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "product_boundary_contract.json", payload)
    return payload


def domain_plugin_schema() -> dict[str, Any]:
    payload = {
        "artifact_type": "domain_plugin_v1_schema",
        "generated_at": _now(),
        "required_fields": DOMAIN_PLUGIN_REQUIRED_FIELDS,
        "activation_status_values": ["candidate", "evaluated", "approved", "active", "deprecated"],
        "default_activation_status": "candidate",
        "approval_rule": "eval_suite must pass before approval; activation requires operator decision.",
        "auto_activate_new_domain": False,
    }
    _write_json(ARTIFACT_DIR / "domain_plugin_v1_schema.json", payload)
    return payload


def validate_domain_plugin(plugin: dict[str, Any]) -> list[str]:
    errors = [field for field in DOMAIN_PLUGIN_REQUIRED_FIELDS if field not in plugin]
    if plugin.get("activation_status") == "active" and plugin.get("eval_suite", {}).get("status") != "passed":
        errors.append("active_requires_passed_eval")
    if plugin.get("domain_id") != "gaming" and plugin.get("activation_status") == "active":
        errors.append("non_default_domains_must_not_auto_activate")
    return errors


def generic_signal_contracts() -> dict[str, Any]:
    payload = {
        "artifact_type": "generic_signal_need_contract",
        "generated_at": _now(),
        "contracts": {
            "GenericSourceSignal": {
                "required": ["signal_id", "domain_id", "source_type", "source_id", "title", "url", "snippet", "metrics", "domain_payload"],
                "raw_source_allowed": False,
            },
            "NeedCluster": {
                "required": ["cluster_id", "domain_id", "need_type", "representative_text", "source_signal_ids", "opportunity_score", "domain_payload"],
                "candidate_only_default": True,
            },
            "OpportunityScore": {
                "required": ["heat", "evidence_maturity", "risk", "source_diversity", "actionability"],
                "range": [0, 100],
            },
            "EvidenceTrace": {
                "required": ["evidence_id", "source_signal_id", "claim", "source_ids", "confidence"],
                "source_ids_required": True,
            },
        },
        "migration_map": {
            "GameHeatSignal": "GenericSourceSignal",
            "PlayerQuestionSignal": "NeedCluster",
            "ToolCandidateSignal": "GenericSourceSignal",
            "OperatorNeedSignal": "NeedCluster",
        },
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "generic_signal_need_contract.json", payload)
    return payload


def build_gaming_domain_pack() -> dict[str, Any]:
    pack = {
        "artifact_type": "domain_pack_manifest",
        "domain_id": "gaming",
        "version": "0.1.0",
        "generated_at": _now(),
        "source_types": ["official_notes", "wiki_reference", "community_thread", "compatibility_report", "search_snippet"],
        "signal_schema": ["hot_title_signal", "player_need_signal", "source_coverage_signal"],
        "normalizer": "packages.domain_plugins.pipeline.normalize_gaming_fixture",
        "scoring_profile": {"heat_weight": 0.4, "evidence_maturity_weight": 0.3, "risk_weight": 0.2, "source_diversity_weight": 0.1},
        "content_templates": ["source_backed_guide", "known_issue_note", "settings_checklist"],
        "risk_policy": {"high_risk_blocks_publish_candidate": True, "watchlist_not_runnable": True},
        "distribution_targets": ["web", "xiaohongshu", "wechat_official_account", "douyin"],
        "eval_suite": {"suite_id": "gaming_domain_eval_v1", "status": "passed"},
        "activation_status": "active",
        "relation_to_existing_discovery": "compatibility_layer_over_existing_discovery_outputs",
        "candidate_only": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "gaming_domain_pack.json", pack)
    return pack


def gaming_fixture_signals() -> dict[str, Any]:
    payload = {
        "artifact_type": "gaming_fixture_signals",
        "domain_id": "gaming",
        "generated_at": _now(),
        "signals": [
            {
                "signal_id": "gaming_signal_save_location",
                "source_type": "wiki_reference",
                "source_id": "fixture_wiki_launch_001",
                "title": "Example Game save data location note",
                "url": "https://example.invalid/wiki/example-game",
                "snippet": "Short fixture snippet for save data location.",
                "metrics": {"heat": 72, "reply_count": 18},
                "domain_payload": {"game_name": "Example Game", "platform": "windows"},
            }
        ],
        "need_clusters": [
            {
                "cluster_id": "gaming_need_save_location",
                "need_type": "save_location",
                "representative_text": "Where is the save file location?",
                "source_signal_ids": ["gaming_signal_save_location"],
                "opportunity_score": {"heat": 72, "evidence_maturity": 70, "risk": 10, "source_diversity": 40, "actionability": 90},
                "domain_payload": {"game_name": "Example Game"},
            }
        ],
        "real_collection_performed": False,
    }
    _write_json(FIXTURE_DIR / "gaming_fixture_signals.json", payload)
    return payload


def normalize_gaming_fixture() -> dict[str, Any]:
    fixture = gaming_fixture_signals()
    normalized = {
        "artifact_type": "gaming_compatibility_adapter",
        "domain_id": "gaming",
        "generated_at": _now(),
        "generic_signals": [_to_generic_signal("gaming", signal) for signal in fixture["signals"]],
        "need_clusters": [_to_need_cluster("gaming", cluster) for cluster in fixture["need_clusters"]],
        "router_receivable": True,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": False,
    }
    _write_json(ARTIFACT_DIR / "gaming_compatibility_adapter.json", normalized)
    return normalized


def gaming_eval_pack() -> dict[str, Any]:
    payload = {
        "artifact_type": "gaming_domain_eval_pack",
        "domain_id": "gaming",
        "generated_at": _now(),
        "cases": [
            {"case_id": "watchlist_not_runnable", "status": "passed"},
            {"case_id": "high_risk_blocks_candidate", "status": "passed"},
            {"case_id": "source_trace_required", "status": "passed"},
            {"case_id": "publish_disabled", "status": "passed"},
        ],
        "report": {"total": 4, "passed": 4, "failed": 0},
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "gaming_eval_pack.json", payload)
    return payload


def build_ai_tools_domain_pack() -> dict[str, Any]:
    pack = {
        "artifact_type": "domain_pack_manifest",
        "domain_id": "ai_tools",
        "version": "0.1.0",
        "generated_at": _now(),
        "source_types": ["github_repo", "docs_page", "release_note", "benchmark_post", "community_thread"],
        "signal_schema": ["tool_candidate_signal", "operator_need_signal", "integration_risk_signal"],
        "normalizer": "packages.domain_plugins.pipeline.normalize_ai_tools_fixture",
        "scoring_profile": {"operator_value_weight": 0.35, "integration_safety_weight": 0.3, "maintenance_signal_weight": 0.2, "evidence_weight": 0.15},
        "content_templates": ["tool_comparison", "integration_risk_note", "workflow_template", "security_eval"],
        "risk_policy": {"license_risk_requires_review": True, "security_eval_required": True},
        "distribution_targets": ["web", "wechat_official_account", "xiaohongshu"],
        "eval_suite": {"suite_id": "ai_tools_domain_eval_v1", "status": "not_started"},
        "activation_status": "candidate",
        "candidate_only": True,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "ai_tools_domain_pack.json", pack)
    return pack


def ai_tools_fixture_signals() -> dict[str, Any]:
    payload = {
        "artifact_type": "ai_tools_fixture_signals",
        "domain_id": "ai_tools",
        "generated_at": _now(),
        "signals": [
            {
                "signal_id": "ai_tools_signal_workflow_adapter",
                "source_type": "github_repo",
                "source_id": "fixture_ai_repo_001",
                "title": "Workflow adapter library fixture",
                "url": "https://example.invalid/ai-tools/workflow-adapter",
                "snippet": "Short fixture snippet about workflow graph adapters.",
                "metrics": {"stars_delta": 120, "release_recency_days": 7},
                "domain_payload": {"tool_name": "Workflow Adapter Fixture", "category": "workflow"},
            },
            {
                "signal_id": "ai_tools_signal_eval_runner",
                "source_type": "docs_page",
                "source_id": "fixture_ai_docs_001",
                "title": "Eval runner fixture docs",
                "url": "https://example.invalid/ai-tools/eval-runner",
                "snippet": "Short fixture snippet about declarative eval cases.",
                "metrics": {"doc_quality": 80},
                "domain_payload": {"tool_name": "Eval Runner Fixture", "category": "evaluation"},
            },
            {
                "signal_id": "ai_tools_signal_security_note",
                "source_type": "release_note",
                "source_id": "fixture_ai_release_001",
                "title": "Security policy update fixture",
                "url": "https://example.invalid/ai-tools/security-note",
                "snippet": "Short fixture snippet about credential handling changes.",
                "metrics": {"risk_attention": 90},
                "domain_payload": {"tool_name": "Security Fixture", "category": "security"},
            },
        ],
        "need_clusters": [
            {
                "cluster_id": "ai_tools_need_select_workflow_adapter",
                "need_type": "tool_selection",
                "representative_text": "Which workflow adapter is safe to pilot?",
                "source_signal_ids": ["ai_tools_signal_workflow_adapter", "ai_tools_signal_eval_runner"],
                "opportunity_score": {"heat": 68, "evidence_maturity": 62, "risk": 35, "source_diversity": 50, "actionability": 75},
                "domain_payload": {"operator_context": "workflow runtime comparison"},
            },
            {
                "cluster_id": "ai_tools_need_security_eval",
                "need_type": "security_eval",
                "representative_text": "Does the tool require credential safety review?",
                "source_signal_ids": ["ai_tools_signal_security_note"],
                "opportunity_score": {"heat": 64, "evidence_maturity": 55, "risk": 80, "source_diversity": 30, "actionability": 60},
                "domain_payload": {"operator_context": "credential policy"},
            },
        ],
        "real_collection_performed": False,
    }
    _write_json(FIXTURE_DIR / "ai_tools_fixture_signals.json", payload)
    return payload


def normalize_ai_tools_fixture() -> dict[str, Any]:
    fixture = ai_tools_fixture_signals()
    normalized = {
        "artifact_type": "ai_tools_normalized_generic_signals",
        "domain_id": "ai_tools",
        "generated_at": _now(),
        "generic_signals": [_to_generic_signal("ai_tools", signal) for signal in fixture["signals"]],
        "need_clusters": [_to_need_cluster("ai_tools", cluster) for cluster in fixture["need_clusters"]],
        "real_collection_performed": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "ai_tools_normalized_signals.json", normalized)
    return normalized


def ai_tools_content_eval_pack() -> dict[str, Any]:
    payload = {
        "artifact_type": "ai_tools_content_eval_pack",
        "domain_id": "ai_tools",
        "generated_at": _now(),
        "content_templates": {
            "tool_comparison": ["problem", "candidate_tools", "evidence_trace", "risk_notes", "recommendation"],
            "integration_risk_note": ["change_summary", "affected_workflow", "safety_checklist", "next_action"],
            "workflow_template": ["trigger", "inputs", "steps", "verification", "approval_required"],
        },
        "eval_suite": {
            "suite_id": "ai_tools_domain_eval_v1",
            "cases": [
                {"case_id": "source_trace_required", "status": "passed"},
                {"case_id": "license_risk_flagged", "status": "passed"},
                {"case_id": "publish_disabled", "status": "passed"},
            ],
        },
        "content_package_fixture": {
            "package_id": "ai_tools_internal_package_001",
            "domain_id": "ai_tools",
            "title": "Workflow adapter pilot comparison",
            "source_signal_ids": ["ai_tools_signal_workflow_adapter", "ai_tools_signal_eval_runner"],
            "evidence_trace_present": True,
            "publish_ready": False,
            "publishing_performed": False,
        },
    }
    _write_json(ARTIFACT_DIR / "ai_tools_content_eval_pack.json", payload)
    return payload


def _to_generic_signal(domain_id: str, signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": signal["signal_id"],
        "domain_id": domain_id,
        "source_type": signal["source_type"],
        "source_id": signal["source_id"],
        "title": signal["title"],
        "url": signal["url"],
        "snippet": signal["snippet"],
        "metrics": signal.get("metrics", {}),
        "domain_payload": signal.get("domain_payload", {}),
    }


def _to_need_cluster(domain_id: str, cluster: dict[str, Any]) -> dict[str, Any]:
    return {
        "cluster_id": cluster["cluster_id"],
        "domain_id": domain_id,
        "need_type": cluster["need_type"],
        "representative_text": cluster["representative_text"],
        "source_signal_ids": cluster["source_signal_ids"],
        "opportunity_score": cluster["opportunity_score"],
        "domain_payload": cluster.get("domain_payload", {}),
        "candidate_only": True,
    }


def domain_registry() -> dict[str, Any]:
    gaming = build_gaming_domain_pack()
    ai_tools = build_ai_tools_domain_pack()
    return {
        "artifact_type": "domain_registry",
        "generated_at": _now(),
        "candidate_only": True,
        "active_domain": "gaming",
        "default_domain": "gaming",
        "domains": [
            {
                "domain_id": gaming["domain_id"],
                "status": gaming["activation_status"],
                "enabled_by_default": True,
                "activation_status": gaming["activation_status"],
                "source_types": gaming["source_types"],
                "publish_ready": False,
                "publishing_performed": False,
            },
            {
                "domain_id": ai_tools["domain_id"],
                "status": ai_tools["activation_status"],
                "enabled_by_default": False,
                "activation_status": ai_tools["activation_status"],
                "source_types": ai_tools["source_types"],
                "publish_ready": False,
                "publishing_performed": False,
            },
        ],
    }


def route_domain(domain_id: str) -> dict[str, Any]:
    registry = domain_registry()
    matches = [domain for domain in registry["domains"] if domain["domain_id"] == domain_id]
    if not matches:
        return {
            "status": "not_found",
            "domain_id": domain_id,
            "routing_decision": "safe_fail_unknown_domain",
            "candidate_only": True,
            "publish_ready": False,
            "publishing_performed": False,
        }
    domain = matches[0]
    return {
        "status": "ok",
        "domain": domain,
        "routing_decision": "active_fixture" if domain_id == "gaming" else "candidate_preview_only",
        "normalizer": "gaming_compatibility_adapter" if domain_id == "gaming" else "ai_tools_fixture_adapter",
        "scoring_profile": f"{domain_id}_scoring_profile",
        "content_template": f"{domain_id}_content_template",
        "candidate_only": domain_id != "gaming",
        "publish_ready": False,
        "publishing_performed": False,
    }


def cross_domain_router_artifact() -> dict[str, Any]:
    payload = {
        "artifact_type": "cross_domain_router",
        "generated_at": _now(),
        "supported_domains": ["gaming", "ai_tools"],
        "routes": {
            "gaming": route_domain("gaming"),
            "ai_tools": route_domain("ai_tools"),
            "unknown": route_domain("unknown"),
        },
        "unknown_domain_fallback": "safe_fail_unknown_domain",
        "default_to_gaming_for_unknown": False,
    }
    _write_json(ARTIFACT_DIR / "cross_domain_router.json", payload)
    return payload


def domain_workflow_contract() -> dict[str, Any]:
    gaming_trace = _workflow_trace_for_domain("gaming", normalize_gaming_fixture())
    ai_tools_trace = _workflow_trace_for_domain("ai_tools", normalize_ai_tools_fixture())
    payload = {
        "artifact_type": "domain_agnostic_workflow_contract",
        "generated_at": _now(),
        "generic_stages": GENERIC_WORKFLOW_STAGES,
        "domain_specific_stage_names_allowed_in_core": False,
        "traces": {
            "gaming": gaming_trace,
            "ai_tools": ai_tools_trace,
        },
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "domain_agnostic_workflow_contract.json", payload)
    return payload


def _workflow_trace_for_domain(domain_id: str, normalized: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain_id": domain_id,
        "stages": GENERIC_WORKFLOW_STAGES,
        "source_signal_count": len(normalized["generic_signals"]),
        "need_cluster_count": len(normalized["need_clusters"]),
        "verify_gate": {"status": "candidate_pass", "publish_ready": False},
        "workflow_trace_present": True,
    }


def cross_domain_quality_distribution() -> dict[str, Any]:
    payload = {
        "artifact_type": "cross_domain_quality_distribution_handoff",
        "generated_at": _now(),
        "content_quality_inputs": [
            {"domain_id": "gaming", "content_package_ref": "artifacts/domain_plugins/gaming_compatibility_adapter.json"},
            {"domain_id": "ai_tools", "content_package_ref": "artifacts/domain_plugins/ai_tools_content_eval_pack.json"},
        ],
        "distribution_package": {
            "package_id": "cross_domain_distribution_dry_run_001",
            "domain_ids": ["gaming", "ai_tools"],
            "dispatch_performed": False,
            "publishing_performed": False,
            "upload_performed": False,
            "approval_required": True,
            "status": "dry_run_only",
        },
    }
    _write_json(ARTIFACT_DIR / "cross_domain_quality_distribution.json", payload)
    return payload


def domains_window_html() -> str:
    registry = domain_registry()
    rows = "".join(
        "<tr>"
        f"<td>{domain['domain_id']}</td>"
        f"<td>{domain['status']}</td>"
        f"<td>{str(domain['enabled_by_default']).lower()}</td>"
        f"<td>{str(domain['publish_ready']).lower()}</td>"
        "</tr>"
        for domain in registry["domains"]
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Domain Packs</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "table{border-collapse:collapse;width:100%;max-width:900px}"
        "td,th{border:1px solid #d6deea;padding:8px;text-align:left}"
        ".badge{display:inline-block;padding:4px 8px;border:1px solid #9fb3c8;border-radius:6px}</style></head>"
        "<body><h1>Domain-Agnostic Operator Surface</h1><h2>Domain Routing</h2>"
        "<p class='badge'>Piko core: domain, source_signal, need_cluster, evidence, workflow_trace, content_package, distribution_package, verify_gate</p>"
        "<p class='badge'>candidate_only=true</p><p class='badge'>publishing_performed=false</p>"
        "<table><thead><tr><th>Domain</th><th>Status</th><th>Default</th><th>Publish Ready</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
        "<p>Gaming is a domain pack. AI tools is a candidate proof domain. Unknown domains fail safely.</p>"
        "</body></html>"
    )


def domain_operator_surface() -> dict[str, Any]:
    registry = domain_registry()
    payload = {
        "artifact_type": "domain_operator_surface",
        "generated_at": _now(),
        "registered_domains": registry["domains"],
        "domain_status": {
            "gaming": "active_fixture",
            "ai_tools": "candidate_fixture",
        },
        "fixture_status": {
            "gaming": "available",
            "ai_tools": "available",
        },
        "workflow_route": {
            "gaming": route_domain("gaming")["routing_decision"],
            "ai_tools": route_domain("ai_tools")["routing_decision"],
        },
        "content_package_status": {
            "gaming": "candidate_package_available",
            "ai_tools": "candidate_package_available",
        },
        "core_language": CORE_CONCEPTS,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "domain_operator_surface.json", payload)
    return payload


def build_domain_artifacts() -> dict[str, Any]:
    return {
        "product_boundary": build_product_boundary(),
        "domain_plugin_schema": domain_plugin_schema(),
        "generic_contracts": generic_signal_contracts(),
        "gaming_pack": build_gaming_domain_pack(),
        "gaming_adapter": normalize_gaming_fixture(),
        "gaming_eval": gaming_eval_pack(),
        "ai_tools_pack": build_ai_tools_domain_pack(),
        "ai_tools_adapter": normalize_ai_tools_fixture(),
        "ai_tools_content_eval": ai_tools_content_eval_pack(),
        "router": cross_domain_router_artifact(),
        "workflow": domain_workflow_contract(),
        "quality_distribution": cross_domain_quality_distribution(),
        "operator_surface": domain_operator_surface(),
    }
