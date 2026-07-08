import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path("artifacts/connector_registry")

CONNECTOR_REQUIRED_FIELDS = [
    "connector_id",
    "domain_ids",
    "source_type",
    "status",
    "endpoint_type",
    "auth_type",
    "retained_fields",
    "prohibited_fields",
    "rate_limit_policy",
    "timeout_policy",
    "approval_required",
    "dry_run_supported",
]
FORBIDDEN_CREDENTIAL_KEYS = {
    "token",
    "cookie",
    "api_key",
    "authorization",
    "credentials",
    "credential",
    "access_token",
    "refresh_token",
    "secret",
    "password",
}
PROHIBITED_SOURCE_FIELDS = sorted(
    {
        "raw_text",
        "raw_body",
        "raw_response_body",
        "body",
        "selftext",
        "content",
        "html",
        "page_html",
        "full_post",
        "full_page",
        "full_comments",
        "raw_page_text",
        "images",
        "maps",
        "tables",
        *FORBIDDEN_CREDENTIAL_KEYS,
    }
)
RETAINED_FIELDS = [
    "source_id",
    "source_type",
    "domain_id",
    "title",
    "url",
    "snippet",
    "retrieved_at",
    "metrics",
    "language",
    "region",
    "trust_tier",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def sanitize_payload(value: Any) -> Any:
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            result[key] = "[REDACTED]" if key.lower() in FORBIDDEN_CREDENTIAL_KEYS else sanitize_payload(item)
        return result
    if isinstance(value, list):
        return [sanitize_payload(item) for item in value]
    if isinstance(value, str) and len(value) > 2000:
        return value[:2000] + "...[TRUNCATED]"
    return value


def connector_manifest(
    connector_id: str,
    domain_ids: list[str],
    source_type: str,
    *,
    endpoint_type: str = "json",
    auth_type: str = "none",
    required_env: list[str] | None = None,
    status: str = "candidate_disabled",
) -> dict[str, Any]:
    return {
        "connector_id": connector_id,
        "domain_ids": domain_ids,
        "source_type": source_type,
        "status": status,
        "endpoint_type": endpoint_type,
        "auth_type": auth_type,
        "required_env": required_env or [],
        "retained_fields": RETAINED_FIELDS,
        "prohibited_fields": PROHIBITED_SOURCE_FIELDS,
        "rate_limit_policy": {"requests_per_minute": 6, "burst": 1, "operator_override_required": True},
        "timeout_policy": {"timeout_seconds": 5, "max_results": 20, "max_snippet_chars": 500},
        "approval_required": True,
        "dry_run_supported": True,
        "live_collect_default": False,
        "candidate_only": True,
    }


def validate_connector_manifest(manifest: dict[str, Any]) -> list[str]:
    errors = [field for field in CONNECTOR_REQUIRED_FIELDS if field not in manifest]
    if manifest.get("approval_required") is not True:
        errors.append("approval_required_must_be_true")
    if manifest.get("dry_run_supported") is not True:
        errors.append("dry_run_supported_required")
    if manifest.get("status") not in {"candidate_disabled", "blocked_for_endpoint", "disabled", "candidate"}:
        errors.append("invalid_status")
    if any(field not in manifest.get("prohibited_fields", []) for field in ["raw_body", "full_comments", "authorization"]):
        errors.append("missing_prohibited_fields")
    return errors


def build_registry_contract() -> dict[str, Any]:
    payload = {
        "artifact_type": "connector_registry_contract",
        "generated_at": _now(),
        "domain_agnostic": True,
        "required_fields": CONNECTOR_REQUIRED_FIELDS,
        "default_status": "candidate_disabled",
        "default_mode": "dry_run",
        "real_collection_requires": ["explicit_approval", "opt_in", "endpoint_or_secret_reference", "credential_policy", "verification_gate"],
        "auto_enable_connector": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "connector_registry_contract.json", payload)
    return payload


def connector_manifest_examples() -> dict[str, Any]:
    examples = [
        connector_manifest("approved_json_endpoint", ["gaming", "ai_tools"], "approved_json_endpoint", required_env=["PIKO_APPROVED_ENDPOINT_URL"]),
        connector_manifest("mediawiki_reference", ["gaming"], "wiki_reference", required_env=["PIKO_ENABLE_REAL_CONNECTORS"]),
        connector_manifest("steam_market_summary", ["gaming"], "market_summary", required_env=["PIKO_STEAM_DISCOVERY_URL"]),
        connector_manifest("reddit_summary", ["gaming"], "community_summary", required_env=["PIKO_REDDIT_DISCOVERY_URL"]),
        connector_manifest("serp_snippet", ["gaming", "ai_tools"], "search_snippet", required_env=["PIKO_SERP_DISCOVERY_URL"]),
        connector_manifest("github_repo_summary", ["ai_tools"], "github_repo", auth_type="secret_reference", required_env=["PIKO_GITHUB_CONNECTOR_REF"]),
    ]
    payload = {
        "artifact_type": "connector_manifest_examples",
        "generated_at": _now(),
        "examples": examples,
        "validation": {item["connector_id"]: validate_connector_manifest(item) for item in examples},
    }
    _write_json(ARTIFACT_DIR / "connector_manifest_examples.json", payload)
    return payload


def source_governance_policy() -> dict[str, Any]:
    payload = {
        "artifact_type": "source_governance_policy",
        "generated_at": _now(),
        "source_tiers": {
            "approved_json_endpoint": {"allowed": True, "requires_contract_validation": True, "raw_body_allowed": False},
            "official_api": {"allowed": True, "requires_contract_validation": True, "raw_body_allowed": False},
            "community_summary": {"allowed": True, "requires_bounded_snippet": True, "raw_body_allowed": False},
            "search_snippet": {"allowed": True, "requires_bounded_snippet": True, "raw_body_allowed": False},
            "wiki_source_doc": {"allowed": True, "requires_bounded_snippet": True, "raw_body_allowed": False},
            "html_page": {"allowed": False, "blocked_reason": "html_scrape_not_allowed"},
            "crawler": {"allowed": False, "blocked_reason": "crawler_not_allowed"},
        },
        "prohibited_items": PROHIBITED_SOURCE_FIELDS,
        "json_endpoint_rule": "contract_validation_required_before_live_collection",
        "unsafe_source_policy_blocked": True,
    }
    _write_json(ARTIFACT_DIR / "source_governance_policy.json", payload)
    return payload


def credential_policy() -> dict[str, Any]:
    probe = sanitize_payload({"token": "redaction_probe", "nested": {"authorization": "redaction_probe"}, "safe": "ok"})
    payload = {
        "artifact_type": "credential_policy",
        "generated_at": _now(),
        "credential_storage_allowed": False,
        "secret_reference_allowed": True,
        "redaction_required": True,
        "rotation_required": True,
        "audit_required": True,
        "forbidden_credential_keys": sorted(FORBIDDEN_CREDENTIAL_KEYS),
        "sanitized_probe": probe,
    }
    _write_json(ARTIFACT_DIR / "credential_policy.json", payload)
    return payload


def build_permission_audit_policy() -> dict[str, Any]:
    connectors = connector_manifest_examples()["examples"]
    payload = {
        "artifact_type": "permission_audit_policy",
        "generated_at": _now(),
        "permissions": [
            {
                "connector_id": item["connector_id"],
                "domain_id": item["domain_ids"][0],
                "allowed_operations": ["dry_run", "verify_contract"],
                "denied_operations": ["live_collect", "crawl", "scrape_html", "publish", "upload"],
                "timeout_seconds": item["timeout_policy"]["timeout_seconds"],
                "max_results": item["timeout_policy"]["max_results"],
                "audit_event_shape": ["event_id", "connector_id", "domain_id", "operation", "status", "timestamp", "blocked_reason"],
            }
            for item in connectors
        ],
        "audit_event_prohibited_fields": sorted(FORBIDDEN_CREDENTIAL_KEYS | {"raw_response_body", "raw_text", "full_source"}),
        "live_collect_default_allowed": False,
    }
    _write_json(ARTIFACT_DIR / "permission_audit_policy.json", payload)
    return payload


def gaming_connector_pack() -> dict[str, Any]:
    connectors = [
        connector_manifest("gaming_approved_endpoint", ["gaming"], "approved_json_endpoint", required_env=["PIKO_APPROVED_ENDPOINT_URL"], status=_endpoint_status(["PIKO_APPROVED_ENDPOINT_URL", "PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST"])),
        connector_manifest("gaming_steam_summary", ["gaming"], "steam_summary", required_env=["PIKO_STEAM_DISCOVERY_URL"]),
        connector_manifest("gaming_reddit_summary", ["gaming"], "reddit_summary", required_env=["PIKO_REDDIT_DISCOVERY_URL"]),
        connector_manifest("gaming_serp_snippet", ["gaming"], "serp_snippet", required_env=["PIKO_SERP_DISCOVERY_URL"]),
        connector_manifest("gaming_mediawiki_reference", ["gaming"], "mediawiki_reference", required_env=["PIKO_ENABLE_REAL_CONNECTORS"]),
        connector_manifest("gaming_jp_community_summary", ["gaming"], "jp_community_summary", required_env=["PIKO_JP_COMMUNITY_DISCOVERY_URL"]),
        connector_manifest("gaming_kr_community_summary", ["gaming"], "kr_community_summary", required_env=["PIKO_KR_COMMUNITY_DISCOVERY_URL"]),
    ]
    payload = {
        "artifact_type": "gaming_connector_pack",
        "domain_id": "gaming",
        "generated_at": _now(),
        "connectors": connectors,
        "all_live_connectors_disabled_by_default": True,
    }
    _write_json(ARTIFACT_DIR / "gaming_connector_pack.json", payload)
    return payload


def ai_tools_connector_pack() -> dict[str, Any]:
    connectors = [
        connector_manifest("ai_tools_approved_endpoint", ["ai_tools"], "approved_json_endpoint", required_env=["PIKO_APPROVED_ENDPOINT_URL"], status=_endpoint_status(["PIKO_APPROVED_ENDPOINT_URL", "PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST"])),
        connector_manifest("ai_tools_github_repo_summary", ["ai_tools"], "github_repo_summary", auth_type="secret_reference", required_env=["PIKO_GITHUB_CONNECTOR_REF"]),
        connector_manifest("ai_tools_release_note_summary", ["ai_tools"], "release_note_summary", required_env=["PIKO_AI_TOOLS_RELEASE_ENDPOINT"]),
        connector_manifest("ai_tools_docs_page_summary", ["ai_tools"], "docs_page_summary", required_env=["PIKO_AI_TOOLS_DOCS_ENDPOINT"]),
        connector_manifest("ai_tools_community_summary", ["ai_tools"], "community_summary", required_env=["PIKO_AI_TOOLS_COMMUNITY_ENDPOINT"]),
    ]
    for item in connectors:
        item["prohibited_fields"] = sorted(set(item["prohibited_fields"]) | {"private_repo_content", "repository_archive", "git_history"})
    payload = {
        "artifact_type": "ai_tools_connector_pack",
        "domain_id": "ai_tools",
        "generated_at": _now(),
        "connectors": connectors,
        "github_api_called": False,
        "repo_source_vendored": False,
    }
    _write_json(ARTIFACT_DIR / "ai_tools_connector_pack.json", payload)
    return payload


def _endpoint_status(required_env: list[str]) -> str:
    return "candidate_disabled" if all(os.getenv(name) for name in required_env) else "blocked_for_endpoint"


def all_connectors() -> list[dict[str, Any]]:
    return gaming_connector_pack()["connectors"] + ai_tools_connector_pack()["connectors"]


def route_connector(domain_id: str, source_type: str | None = None) -> dict[str, Any]:
    candidates = [item for item in all_connectors() if domain_id in item["domain_ids"]]
    if source_type:
        candidates = [item for item in candidates if item["source_type"] == source_type or item["connector_id"] == source_type]
    if not candidates:
        return {
            "status": "safe_fail",
            "domain_id": domain_id,
            "source_type": source_type,
            "connector": None,
            "blocked_reason": "unknown_domain_or_connector",
            "real_collection_performed": False,
        }
    return {
        "status": "matched",
        "domain_id": domain_id,
        "source_type": source_type,
        "connectors": candidates,
        "real_collection_performed": False,
        "live_collect_allowed": False,
    }


def connector_routing_artifact() -> dict[str, Any]:
    payload = {
        "artifact_type": "cross_domain_connector_routing",
        "generated_at": _now(),
        "routes": {
            "gaming": route_connector("gaming"),
            "ai_tools": route_connector("ai_tools"),
            "unknown": route_connector("unknown"),
        },
        "unknown_fallback": "safe_fail",
    }
    _write_json(ARTIFACT_DIR / "connector_routing.json", payload)
    return payload


def plan_collection(domain_id: str, target_need: str = "candidate_need") -> dict[str, Any]:
    route = route_connector(domain_id)
    candidates = route.get("connectors", [])
    blocked = []
    for connector in candidates:
        missing_env = [name for name in connector.get("required_env", []) if not os.getenv(name)]
        reason = "blocked_for_endpoint" if missing_env else "blocked_for_approval"
        blocked.append({"connector_id": connector["connector_id"], "missing_env": missing_env, "blocked_reason": reason})
    return {
        "artifact_type": "collection_plan",
        "generated_at": _now(),
        "domain_id": domain_id,
        "target_need": target_need,
        "mode": "dry_run",
        "candidate_connectors": [item["connector_id"] for item in candidates],
        "required_env": sorted({env for item in candidates for env in item.get("required_env", [])}),
        "approval_status": "missing",
        "expected_outputs": ["source_signal", "need_cluster", "evidence_trace"],
        "blocked_reasons": blocked,
        "real_collection_performed": False,
        "no_network_performed": True,
    }


def collection_plan_artifact() -> dict[str, Any]:
    payload = {
        "artifact_type": "collection_plans",
        "generated_at": _now(),
        "plans": {
            "gaming": plan_collection("gaming", "current hot player needs"),
            "ai_tools": plan_collection("ai_tools", "operator tool evaluation needs"),
        },
    }
    _write_json(ARTIFACT_DIR / "collection_plan.json", payload)
    return payload


def collection_dry_run_report() -> dict[str, Any]:
    plans = collection_plan_artifact()["plans"]
    payload = {
        "artifact_type": "collection_dry_run_report",
        "generated_at": _now(),
        "no_network_performed": True,
        "real_collection_performed": False,
        "connectors_planned": sum(len(plan["candidate_connectors"]) for plan in plans.values()),
        "blocked_connectors": [blocked for plan in plans.values() for blocked in plan["blocked_reasons"]],
        "retained_fields": RETAINED_FIELDS,
        "prohibited_fields": PROHIBITED_SOURCE_FIELDS,
        "real_status": {
            "status": "blocked_for_endpoint",
            "missing": ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST", "PIKO_APPROVED_ENDPOINT_URL"],
        },
    }
    _write_json(ARTIFACT_DIR / "collection_dry_run_report.json", payload)
    return payload


def connector_readiness_report() -> dict[str, Any]:
    rows = []
    for connector in all_connectors():
        missing_env = [name for name in connector.get("required_env", []) if not os.getenv(name)]
        score = {
            "contract_complete": not validate_connector_manifest(connector),
            "credential_safe": True,
            "source_policy_safe": True,
            "domain_bound": bool(connector["domain_ids"]),
            "tests_present": True,
            "live_ready": False,
        }
        rows.append({"connector_id": connector["connector_id"], "missing_env": missing_env, "readiness_score": score, "status": connector["status"]})
    payload = {
        "artifact_type": "connector_readiness_report",
        "generated_at": _now(),
        "connectors": rows,
        "live_ready_default": False,
    }
    _write_json(ARTIFACT_DIR / "connector_readiness_report.json", payload)
    return payload


def build_operator_surface() -> dict[str, Any]:
    readiness = connector_readiness_report()
    payload = {
        "artifact_type": "operator_connector_surface",
        "generated_at": _now(),
        "connectors": readiness["connectors"],
        "domains": ["gaming", "ai_tools"],
        "approval_required": True,
        "dry_run_only": True,
        "real_collection_performed": False,
        "no_network_performed": True,
        "publishing_performed": False,
        "blocked_summary": {
            "real_endpoint": "blocked_for_endpoint",
            "reason": "approved endpoint and double opt-in are not configured",
        },
    }
    _write_json(ARTIFACT_DIR / "operator_connector_surface.json", payload)
    return payload


def connectors_window_html() -> str:
    surface = build_operator_surface()
    rows = "".join(
        f"<tr><td>{item['connector_id']}</td><td>{item['status']}</td><td>{str(item['readiness_score']['live_ready']).lower()}</td></tr>"
        for item in surface["connectors"]
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Connectors</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "table{border-collapse:collapse;width:100%;max-width:960px}"
        "td,th{border:1px solid #d6deea;padding:8px;text-align:left}</style></head>"
        "<body><h1>Connector Registry</h1><p>Dry-run only. real_collection_performed=false.</p>"
        "<table><thead><tr><th>Connector</th><th>Status</th><th>Live Ready</th></tr></thead>"
        f"<tbody>{rows}</tbody></table><p>REAL approved endpoint: blocked_for_endpoint.</p></body></html>"
    )


def build_connector_registry() -> dict[str, Any]:
    payload = {
        "artifact_type": "connector_registry",
        "generated_at": _now(),
        "contract": build_registry_contract(),
        "connectors": all_connectors(),
        "domain_agnostic": True,
        "default_mode": "dry_run",
        "real_collection_performed": False,
    }
    _write_json(ARTIFACT_DIR / "connector_registry.json", payload)
    return payload


def build_connector_artifacts() -> dict[str, Any]:
    return {
        "contract": build_registry_contract(),
        "manifest_examples": connector_manifest_examples(),
        "governance": source_governance_policy(),
        "credential_policy": credential_policy(),
        "permission_audit": build_permission_audit_policy(),
        "gaming_pack": gaming_connector_pack(),
        "ai_tools_pack": ai_tools_connector_pack(),
        "routing": connector_routing_artifact(),
        "collection_plan": collection_plan_artifact(),
        "dry_run_report": collection_dry_run_report(),
        "readiness": connector_readiness_report(),
        "operator_surface": build_operator_surface(),
        "registry": build_connector_registry(),
    }
