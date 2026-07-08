import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.external_endpoint.pipeline import (
    BLOCKED,
    EXTERNAL_SCOPE,
    SUCCESS,
    build_external_endpoint_artifacts,
    external_endpoint_readiness,
    external_http_probe,
)


ARTIFACT_DIR = Path("artifacts/final_mvp")
LATEST_EXTERNAL_LIVE_RESULT = ARTIFACT_DIR / "latest_external_live_result.json"
LATEST_REAL_SIGNAL_FUNNEL = ARTIFACT_DIR / "latest_real_signal_funnel.json"
LATEST_CONTENT_PACKAGE = ARTIFACT_DIR / "latest_content_package.json"
LATEST_OPERATOR_CONSOLE = ARTIFACT_DIR / "latest_operator_console.json"
LATEST_PUBLISH_DISTRIBUTION_PLAN = ARTIFACT_DIR / "latest_publish_distribution_plan.json"
LATEST_MVP_READINESS = ARTIFACT_DIR / "latest_mvp_readiness.json"
BLOCKED_FOR_EXTERNAL_ENDPOINT = "blocked_for_external_endpoint"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _success_from_probe(probe: dict[str, Any]) -> bool:
    return probe.get("status") == SUCCESS and probe.get("real_collection_performed") is True


def external_live_result(external_artifacts: dict[str, Any] | None = None) -> dict[str, Any]:
    readiness = (external_artifacts or {}).get("readiness") or external_endpoint_readiness()
    probe = (external_artifacts or {}).get("probe") or external_http_probe()
    success = _success_from_probe(probe)
    status = SUCCESS if success else BLOCKED_FOR_EXTERNAL_ENDPOINT
    blocked_reason = None if success else probe.get("blocked_reason") or readiness.get("blocked_reason")
    result = {
        "artifact_type": "final_mvp_external_live_result",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": status,
        "external_endpoint_status": probe.get("status"),
        "readiness_status": readiness.get("status"),
        "blocked_reason": blocked_reason,
        "missing_config": readiness.get("missing_config", []),
        "endpoint_url_present": readiness.get("endpoint_url_present", False),
        "endpoint_scheme": readiness.get("endpoint_scheme"),
        "endpoint_host": readiness.get("endpoint_host"),
        "endpoint_url_stored": False,
        "double_opt_in_configured": readiness.get("double_opt_in_configured", False),
        "real_collection_performed": bool(success),
        "normalized_game_count": probe.get("normalized_game_count", 0),
        "normalized_question_count": probe.get("normalized_question_count", 0),
        "retained_fields": probe.get("retained_fields", []),
        "raw_response_body_saved": False,
        "full_posts_saved": False,
        "full_pages_saved": False,
        "full_comments_saved": False,
        "credentials_stored": False,
        "secrets_retained": False,
        "crawler_used": False,
        "html_scrape_used": False,
        "llm_called": False,
        "broad_internet_coverage": False,
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "candidate_only": True,
        "next_action": "configure_external_approved_endpoint_and_rerun_finish"
        if not success
        else "continue_finish_real_signal_funnel",
    }
    _write_json(LATEST_EXTERNAL_LIVE_RESULT, result)
    return result


def real_signal_funnel(external_artifacts: dict[str, Any]) -> dict[str, Any]:
    live = external_live_result(external_artifacts)
    handoff = external_artifacts.get("handoff", {})
    probe = external_artifacts.get("probe", {})
    success = live["real_collection_performed"] is True
    ranking_preview = probe.get("ranking_preview", {}) if success else {}
    pain_buckets = handoff.get("pain_buckets", {}) if success else {}
    artifact = {
        "artifact_type": "final_mvp_real_signal_funnel",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "completed" if success else BLOCKED_FOR_EXTERNAL_ENDPOINT,
        "mode": "real-source" if success else "blocked",
        "domain_routing": {
            "domain_id": "gaming" if success else None,
            "routing_decision": "route_to_gaming_domain_pack" if success else "blocked_no_live_signal",
            "core_concepts": ["domain", "source_signal", "need_cluster", "evidence", "workflow_trace"],
            "domain_pack_auto_activated": False,
        },
        "top_hot_games": ranking_preview.get("top_hot_games", []),
        "topic_buckets": pain_buckets,
        "source_trace": handoff.get("source_trace", []),
        "real_collection_performed": bool(success),
        "publish_ready": False,
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(LATEST_REAL_SIGNAL_FUNNEL, artifact)
    return artifact


def content_package(external_artifacts: dict[str, Any], funnel: dict[str, Any] | None = None) -> dict[str, Any]:
    live = external_live_result(external_artifacts)
    funnel = funnel or real_signal_funnel(external_artifacts)
    candidate_package = external_artifacts.get("candidate_package", {})
    selected = candidate_package.get("selected_topic")
    success = live["real_collection_performed"] is True and selected is not None
    source_trace = candidate_package.get("source_trace", [])
    source_id = (source_trace[0] if source_trace else {}).get("source_id")
    question_id = (selected or {}).get("question_id")
    evidence_cards = []
    ranked_claims = []
    if success:
        evidence_cards = [
            {
                "evidence_card_id": f"finish_ev_{question_id}",
                "source_id": source_id,
                "claim_type": "candidate_signal",
                "claim": (selected or {}).get("question_text"),
                "confidence": (selected or {}).get("evidence_quality", 0),
                "risk_note": f"Risk level: {(selected or {}).get('risk_level')}; needs page-level evidence before publishing.",
            }
        ]
        ranked_claims = [
            {
                "rank": 1,
                "claim": (selected or {}).get("question_text"),
                "source_ids": [source_id],
                "evidence_card_ids": [evidence_cards[0]["evidence_card_id"]],
                "needs_more_evidence": True,
            }
        ]
    artifact = {
        "artifact_type": "final_mvp_content_package",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "internal_candidate_package" if success else BLOCKED_FOR_EXTERNAL_ENDPOINT,
        "selected_topic": selected,
        "source_trace": source_trace,
        "evidence_cards": evidence_cards,
        "ranked_claims": ranked_claims,
        "writer_input": {
            "game_name": (selected or {}).get("game_name"),
            "player_question": (selected or {}).get("question_text"),
            "source_ids": [source_id] if source_id else [],
            "evidence_card_ids": [card["evidence_card_id"] for card in evidence_cards],
            "instruction": "Prepare internal brief only; do not publish.",
        },
        "quality_package": {
            "headline_hook_present": bool(selected),
            "intro_directness": "candidate_signal_only",
            "source_trace_present": bool(source_trace),
            "evidence_trace_present": bool(evidence_cards),
            "media_plan_present": True,
            "image_generation_performed": False,
        },
        "media_plan": {
            "external_media_used": False,
            "image_generation_performed": False,
            "recommended_media": ["Operator-owned screenshot only after future explicit approval."],
        },
        "verification_required": True,
        "real_collection_performed": live["real_collection_performed"],
        "publish_ready": False,
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
        "upstream_funnel_status": funnel["status"],
    }
    _write_json(LATEST_CONTENT_PACKAGE, artifact)
    return artifact


def human_approval_contract() -> dict[str, Any]:
    return {
        "approval_required_for": [
            "publish",
            "upload",
            "deploy",
            "credential_use",
            "external_connector_activation",
            "active_plugin_replacement",
            "paid_service_use",
        ],
        "default_state": "blocked_for_human_approval",
        "approval_granted": False,
        "credential_storage_allowed": False,
        "publishing_performed": False,
    }


def operator_console(
    external_artifacts: dict[str, Any],
    funnel: dict[str, Any] | None = None,
    package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    live = external_live_result(external_artifacts)
    funnel = funnel or real_signal_funnel(external_artifacts)
    package = package or content_package(external_artifacts, funnel)
    artifact = {
        "artifact_type": "final_mvp_operator_console",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "ready_for_operator_review" if live["real_collection_performed"] else BLOCKED_FOR_EXTERNAL_ENDPOINT,
        "external_endpoint": live,
        "real_signal_funnel": {
            "status": funnel["status"],
            "top_hot_games_count": len(funnel.get("top_hot_games", [])),
            "topic_bucket_keys": sorted((funnel.get("topic_buckets") or {}).keys()),
        },
        "content_package": {
            "status": package["status"],
            "selected_topic": package.get("selected_topic"),
            "source_trace_present": bool(package.get("source_trace")),
            "evidence_trace_present": bool(package.get("evidence_cards")),
        },
        "approval_contract": human_approval_contract(),
        "read_only_surface": True,
        "real_collection_performed": live["real_collection_performed"],
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(LATEST_OPERATOR_CONSOLE, artifact)
    return artifact


def publish_distribution_plan(package: dict[str, Any] | None = None) -> dict[str, Any]:
    if package is None:
        package = json.loads(LATEST_CONTENT_PACKAGE.read_text(encoding="utf-8")) if LATEST_CONTENT_PACKAGE.exists() else {}
    platforms = ["xiaohongshu", "wechat_official_account", "douyin", "web"]
    artifact = {
        "artifact_type": "final_mvp_publish_distribution_plan",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "dry_run_package_ready" if package.get("selected_topic") else BLOCKED_FOR_EXTERNAL_ENDPOINT,
        "platform_packages": [
            {
                "platform": platform,
                "package_type": "dry_run_preview",
                "approval_required": True,
                "credential_required_before_dispatch": True,
                "dispatch_performed": False,
                "upload_performed": False,
                "publishing_performed": False,
            }
            for platform in platforms
        ],
        "required_credentials": ["platform_operator_credential_not_stored"],
        "human_approval_required": True,
        "approval_granted": False,
        "credential_storage_performed": False,
        "real_collection_performed": bool(package.get("real_collection_performed")),
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(LATEST_PUBLISH_DISTRIBUTION_PLAN, artifact)
    return artifact


def mvp_readiness(
    live: dict[str, Any] | None = None,
    funnel: dict[str, Any] | None = None,
    package: dict[str, Any] | None = None,
    console: dict[str, Any] | None = None,
    distribution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    live = live or (json.loads(LATEST_EXTERNAL_LIVE_RESULT.read_text(encoding="utf-8")) if LATEST_EXTERNAL_LIVE_RESULT.exists() else {})
    funnel = funnel or (json.loads(LATEST_REAL_SIGNAL_FUNNEL.read_text(encoding="utf-8")) if LATEST_REAL_SIGNAL_FUNNEL.exists() else {})
    package = package or (json.loads(LATEST_CONTENT_PACKAGE.read_text(encoding="utf-8")) if LATEST_CONTENT_PACKAGE.exists() else {})
    console = console or (json.loads(LATEST_OPERATOR_CONSOLE.read_text(encoding="utf-8")) if LATEST_OPERATOR_CONSOLE.exists() else {})
    distribution = distribution or (
        json.loads(LATEST_PUBLISH_DISTRIBUTION_PLAN.read_text(encoding="utf-8"))
        if LATEST_PUBLISH_DISTRIBUTION_PLAN.exists()
        else {}
    )
    success = live.get("real_collection_performed") is True
    artifact = {
        "artifact_type": "final_mvp_readiness",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "mvp_ready_for_verify" if success else BLOCKED_FOR_EXTERNAL_ENDPOINT,
        "external_endpoint_success": success,
        "real_collection_performed": success,
        "contract_validation_passed": live.get("external_endpoint_status") == SUCCESS,
        "domain_router_connected": funnel.get("domain_routing", {}).get("routing_decision") == "route_to_gaming_domain_pack",
        "topic_funnel_connected": bool(funnel.get("topic_buckets")),
        "content_package_connected": bool(package.get("source_trace")) and bool(package.get("evidence_cards")),
        "operator_console_connected": console.get("read_only_surface") is True,
        "distribution_plan_connected": bool(distribution.get("platform_packages")),
        "requires_human_approval_before_publish": True,
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "raw_response_body_saved": False,
        "full_posts_saved": False,
        "full_pages_saved": False,
        "full_comments_saved": False,
        "credentials_stored": False,
        "secrets_retained": False,
        "crawler_used": False,
        "html_scrape_used": False,
        "llm_called": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
        "next_action": "piko_verify_finish_external_success" if success else "configure_external_approved_endpoint_and_rerun_finish",
    }
    _write_json(LATEST_MVP_READINESS, artifact)
    return artifact


def build_finish_gate_artifacts() -> dict[str, Any]:
    external_artifacts = build_external_endpoint_artifacts()
    live = external_live_result(external_artifacts)
    if live["real_collection_performed"] is not True:
        return {"external_live_result": live}
    funnel = real_signal_funnel(external_artifacts)
    package = content_package(external_artifacts, funnel)
    console = operator_console(external_artifacts, funnel, package)
    distribution = publish_distribution_plan(package)
    readiness = mvp_readiness(live, funnel, package, console, distribution)
    return {
        "external_live_result": live,
        "real_signal_funnel": funnel,
        "content_package": package,
        "operator_console": console,
        "publish_distribution_plan": distribution,
        "mvp_readiness": readiness,
    }


def operator_window_html() -> str:
    console = json.loads(LATEST_OPERATOR_CONSOLE.read_text(encoding="utf-8")) if LATEST_OPERATOR_CONSOLE.exists() else {}
    readiness = json.loads(LATEST_MVP_READINESS.read_text(encoding="utf-8")) if LATEST_MVP_READINESS.exists() else {}
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Final MVP</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "dl{display:grid;grid-template-columns:240px minmax(0,1fr);gap:8px;max-width:980px}"
        "dt{font-weight:700}dd{margin:0}.ok{color:#166534}.blocked{color:#9f1239}</style></head>"
        "<body><h1>Final MVP Operator Console</h1>"
        "<p>Read-only review surface. No publish, upload, deploy, crawler, raw source, or LLM path is active.</p><dl>"
        f"<dt>Status</dt><dd>{readiness.get('status', console.get('status', 'missing'))}</dd>"
        f"<dt>Scope</dt><dd>{readiness.get('scope', EXTERNAL_SCOPE)}</dd>"
        f"<dt>Real collection performed</dt><dd>{str(readiness.get('real_collection_performed', False)).lower()}</dd>"
        f"<dt>Publish ready</dt><dd>{str(readiness.get('publish_ready', False)).lower()}</dd>"
        f"<dt>Publishing performed</dt><dd>{str(readiness.get('publishing_performed', False)).lower()}</dd>"
        f"<dt>Human approval required</dt><dd>{str(readiness.get('requires_human_approval_before_publish', True)).lower()}</dd>"
        "</dl></body></html>"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Piko FINISH external endpoint gate.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write FINISH gate artifacts.")
    args = parser.parse_args()
    result = build_finish_gate_artifacts() if args.write_artifacts else external_live_result()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
