import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from packages.collectors.real_market import (
    JPCommunityMarketConnector,
    KRCommunityMarketConnector,
    RedditMarketConnector,
    SERPMarketConnector,
    SteamMarketConnector,
)
from packages.discovery.rankings import rank_hot_games
from packages.discovery.real_market import (
    MAX_SNIPPET_CHARS,
    REAL_MARKET_ENDPOINT_ENV_VARS,
    REAL_MARKET_PROHIBITED_RETENTION,
    REAL_MARKET_REQUIRED_HOT_GAME_FIELDS,
    REAL_MARKET_REQUIRED_PLAYER_QUESTION_FIELDS,
    REAL_MARKET_RETAINED_FIELDS,
    REAL_MARKET_SOURCE_CATEGORIES,
    RealMarketConfigError,
    RealMarketSourceCategory,
    endpoint_config,
    real_market_source_contract,
)
from packages.shared.config import get_settings


ARTIFACT_DIR = Path("artifacts/realdata")
LATEST_PROVIDER_CONTRACT = ARTIFACT_DIR / "latest_provider_contract.json"
LATEST_PROVIDER_COLLECTION = ARTIFACT_DIR / "latest_provider_collection.json"
LATEST_PROVIDER_FRESHNESS = ARTIFACT_DIR / "latest_provider_freshness.json"
LATEST_REALDATA_FUNNEL = ARTIFACT_DIR / "latest_realdata_funnel.json"
LATEST_REALDATA_CONTENT_PACKAGE = ARTIFACT_DIR / "latest_realdata_content_package.json"
LATEST_REALDATA_OPERATOR_RESULT = ARTIFACT_DIR / "latest_realdata_operator_result.json"
LATEST_REALDATA_READINESS = ARTIFACT_DIR / "latest_realdata_readiness.json"

BLOCKED = "blocked_for_provider_endpoints"
PARTIAL = "partial_real_provider_coverage"
READY = "provider_coverage_ready"
FAILED = "failed_contract_validation"
PROVIDERS: list[RealMarketSourceCategory] = ["steam", "reddit", "serp_snippet", "jp_community", "kr_community"]
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _endpoint_for(provider: RealMarketSourceCategory) -> str | None:
    return endpoint_config().get(provider)


def _endpoint_status(url: str | None) -> tuple[str, str | None]:
    if not url:
        return "missing", "missing_provider_endpoint"
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "rejected", "endpoint_must_be_http_or_https"
    if (parsed.hostname or "").lower() in LOCAL_HOSTS:
        return "rejected", "localhost_not_allowed_for_provider_endpoint"
    return "ready", None


def provider_contract() -> dict[str, Any]:
    base = real_market_source_contract()
    providers = []
    for provider in PROVIDERS:
        providers.append(
            {
                "provider_id": provider,
                "endpoint_env_var": REAL_MARKET_ENDPOINT_ENV_VARS[provider],
                "endpoint_type": "approved_json_summary_endpoint",
                "required_hot_game_fields": REAL_MARKET_REQUIRED_HOT_GAME_FIELDS,
                "required_player_question_fields": REAL_MARKET_REQUIRED_PLAYER_QUESTION_FIELDS,
                "retained_fields": REAL_MARKET_RETAINED_FIELDS[provider],
                "prohibited_fields": REAL_MARKET_PROHIBITED_RETENTION,
                "max_snippet_chars": MAX_SNIPPET_CHARS,
                "candidate_only": True,
                "enabled_by_default": False,
            }
        )
    artifact = {
        "artifact_type": "realdata_provider_contract",
        "generated_at": _now(),
        "providers": providers,
        "source_contract": base,
        "default_network_disabled": True,
        "approval_required": True,
        "crawler_allowed": False,
        "html_scrape_allowed": False,
        "raw_full_source_retention_allowed": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(LATEST_PROVIDER_CONTRACT, artifact)
    return artifact


def provider_readiness() -> dict[str, Any]:
    settings = get_settings()
    provider_rows = []
    ready_count = 0
    for provider in PROVIDERS:
        url = _endpoint_for(provider)
        status, reason = _endpoint_status(url)
        if status == "ready":
            ready_count += 1
        parsed = urlparse(url or "")
        provider_rows.append(
            {
                "provider_id": provider,
                "endpoint_env_var": REAL_MARKET_ENDPOINT_ENV_VARS[provider],
                "endpoint_configured": bool(url),
                "endpoint_status": status,
                "blocked_reason": reason,
                "endpoint_scheme": parsed.scheme or None,
                "endpoint_host": parsed.hostname,
                "endpoint_url_stored": False,
            }
        )
    opt_in_ready = settings.enable_discovery_real_source and settings.live_discovery_test
    if not opt_in_ready or ready_count == 0:
        coverage_status = BLOCKED
    elif ready_count < 2:
        coverage_status = PARTIAL
    else:
        coverage_status = READY
    artifact = {
        "artifact_type": "realdata_provider_readiness",
        "generated_at": _now(),
        "coverage_status": coverage_status,
        "opt_in_ready": opt_in_ready,
        "required_flags": ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true", "PIKO_LIVE_DISCOVERY_TEST=true"],
        "provider_count": len(PROVIDERS),
        "ready_provider_count": ready_count,
        "provider_statuses": provider_rows,
        "real_collection_performed": False,
        "broad_internet_coverage": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    return artifact


def _connector_for(provider: RealMarketSourceCategory):
    return {
        "steam": SteamMarketConnector,
        "reddit": RedditMarketConnector,
        "serp_snippet": SERPMarketConnector,
        "jp_community": JPCommunityMarketConnector,
        "kr_community": KRCommunityMarketConnector,
    }[provider]


def collect_providers(query: str = "game player questions", limit_per_source: int = 5) -> dict[str, Any]:
    contract = provider_contract()
    readiness = provider_readiness()
    provider_results = []
    hot_games = []
    questions = []
    source_summary = []

    if readiness["coverage_status"] == BLOCKED:
        artifact = {
            "artifact_type": "realdata_provider_collection",
            "generated_at": _now(),
            "coverage_status": BLOCKED,
            "provider_statuses": readiness["provider_statuses"],
            "hot_games": [],
            "player_questions": [],
            "source_summary": [],
            "provider_results": [],
            "blocked_reason": "No approved provider endpoints or live opt-in are configured.",
            "real_collection_performed": False,
            "broad_internet_coverage": False,
            "raw_response_body_saved": False,
            "publish_ready": False,
            "publishing_performed": False,
            "candidate_only": True,
        }
        _write_json(LATEST_PROVIDER_COLLECTION, artifact)
        return artifact

    for row in readiness["provider_statuses"]:
        provider = row["provider_id"]
        if row["endpoint_status"] != "ready":
            provider_results.append({**row, "collection_status": "blocked_for_provider_endpoint", "real_collection_performed": False})
            continue
        try:
            result = _connector_for(provider)().collect(query=query, limit_per_source=limit_per_source)
            games = [item.model_dump(mode="json") for item in result.hot_games]
            qrows = [item.model_dump(mode="json") for item in result.player_questions]
            hot_games.extend(games)
            questions.extend(qrows)
            source_summary.extend([item.model_dump(mode="json") for item in result.source_summary])
            provider_results.append(
                {
                    **row,
                    "collection_status": "success",
                    "hot_game_count": len(games),
                    "player_question_count": len(qrows),
                    "real_collection_performed": True,
                }
            )
        except RealMarketConfigError as exc:
            provider_results.append(
                {**row, "collection_status": FAILED, "blocked_reason": str(exc), "real_collection_performed": False}
            )

    success_count = sum(1 for item in provider_results if item.get("collection_status") == "success")
    coverage_status = BLOCKED if success_count == 0 else PARTIAL if success_count < 2 else READY
    artifact = {
        "artifact_type": "realdata_provider_collection",
        "generated_at": _now(),
        "coverage_status": coverage_status,
        "contract_ref": str(LATEST_PROVIDER_CONTRACT),
        "provider_statuses": readiness["provider_statuses"],
        "provider_results": provider_results,
        "hot_games": hot_games,
        "player_questions": questions,
        "source_summary": source_summary,
        "successful_provider_count": success_count,
        "coverage_limits": [item["provider_id"] for item in provider_results if item.get("collection_status") == "success"],
        "real_collection_performed": success_count > 0,
        "broad_internet_coverage": False,
        "raw_response_body_saved": False,
        "publish_ready": False,
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(LATEST_PROVIDER_COLLECTION, artifact)
    return artifact


def provider_freshness(collection: dict[str, Any] | None = None) -> dict[str, Any]:
    collection = collection or collect_providers()
    rows = []
    for item in collection.get("player_questions", []):
        observed = item.get("created_at") or item.get("metadata", {}).get("observed_at")
        rows.append(
            {
                "provider_id": item.get("source_type"),
                "question_id": item.get("question_id"),
                "source_category": item.get("source_type"),
                "source_url": item.get("url"),
                "observed_at": observed,
                "fetched_at": collection["generated_at"],
                "freshness_status": "unknown" if not observed else "recent",
            }
        )
    artifact = {
        "artifact_type": "realdata_provider_freshness",
        "generated_at": _now(),
        "coverage_status": collection["coverage_status"],
        "freshness_rows": rows,
        "stale_records_block_high_priority": True,
        "real_collection_performed": collection.get("real_collection_performed", False),
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(LATEST_PROVIDER_FRESHNESS, artifact)
    return artifact


def realdata_funnel(collection: dict[str, Any] | None = None) -> dict[str, Any]:
    collection = collection or collect_providers()
    if collection["coverage_status"] == BLOCKED:
        artifact = {
            "artifact_type": "realdata_funnel",
            "generated_at": _now(),
            "coverage_status": BLOCKED,
            "top_hot_games": [],
            "question_buckets": {},
            "selected_topic": None,
            "no_candidate_reason": "blocked_for_provider_endpoints",
            "real_collection_performed": False,
            "publish_ready": False,
            "publishing_performed": False,
            "broad_internet_coverage": False,
            "candidate_only": True,
        }
        _write_json(LATEST_REALDATA_FUNNEL, artifact)
        return artifact

    top_games = rank_hot_games([type("Obj", (), item)() for item in []], mode="real-source", limit=5)
    # Re-rank with lightweight dict rows if the pydantic objects are unavailable here.
    top_games = sorted(collection.get("hot_games", []), key=lambda row: row.get("heat_score", 0), reverse=True)[:5]
    questions = collection.get("player_questions", [])
    answered = [q for q in questions if q.get("metadata", {}).get("answer_maturity") == "answered" and q.get("risk_level") != "high"]
    watchlist = [q for q in questions if q.get("metadata", {}).get("answer_maturity") in {"unanswered", "unknown"}]
    conflict = [q for q in questions if q.get("answer_conflict_count", 0) or q.get("metadata", {}).get("answer_maturity") == "conflicting"]
    high_risk = [q for q in questions if q.get("risk_level") == "high"]
    selected = sorted(answered, key=lambda q: (q.get("engagement_count", 0), q.get("evidence_quality", 0)), reverse=True)[:1]
    artifact = {
        "artifact_type": "realdata_funnel",
        "generated_at": _now(),
        "coverage_status": collection["coverage_status"],
        "coverage_limits": collection.get("coverage_limits", []),
        "top_hot_games": top_games,
        "question_buckets": {
            "answered_candidates": answered[:5],
            "watchlist_topics": watchlist[:5],
            "conflict_topics": conflict[:5],
            "high_risk_blocked_topics": high_risk[:5],
        },
        "selected_topic": selected[0] if selected else None,
        "no_candidate_reason": None if selected else "no_answered_low_risk_topic",
        "real_collection_performed": collection.get("real_collection_performed", False),
        "publish_ready": False,
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(LATEST_REALDATA_FUNNEL, artifact)
    return artifact


def content_package(funnel: dict[str, Any] | None = None) -> dict[str, Any]:
    funnel = funnel or realdata_funnel()
    selected = funnel.get("selected_topic")
    evidence = []
    if selected:
        evidence = [
            {
                "evidence_card_id": f"realdata_ev_{selected.get('question_id')}",
                "provider_id": selected.get("source_type"),
                "source_id": selected.get("metadata", {}).get("source_category") or selected.get("source_type"),
                "claim": selected.get("question_text"),
                "snippet": selected.get("snippet"),
                "risk_note": f"Risk level: {selected.get('risk_level')}; page-level verification required.",
            }
        ]
    artifact = {
        "artifact_type": "realdata_content_package",
        "generated_at": _now(),
        "coverage_status": funnel["coverage_status"],
        "selected_topic": selected,
        "source_trace": [] if not selected else [{"provider_id": selected.get("source_type"), "url": selected.get("url")}],
        "evidence_cards": evidence,
        "writer_input": None
        if not selected
        else {
            "game_name": selected.get("game_name"),
            "player_question": selected.get("question_text"),
            "provider_ids": [selected.get("source_type")],
            "evidence_card_ids": [e["evidence_card_id"] for e in evidence],
            "instruction": "Internal candidate only; do not publish.",
        },
        "verification_required": True,
        "real_collection_performed": funnel.get("real_collection_performed", False),
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "candidate_only": True,
    }
    _write_json(LATEST_REALDATA_CONTENT_PACKAGE, artifact)
    return artifact


def operator_result(collection: dict[str, Any] | None = None, funnel: dict[str, Any] | None = None, package: dict[str, Any] | None = None) -> dict[str, Any]:
    collection = collection or collect_providers()
    funnel = funnel or realdata_funnel(collection)
    package = package or content_package(funnel)
    artifact = {
        "artifact_type": "realdata_operator_result",
        "generated_at": _now(),
        "coverage_status": collection["coverage_status"],
        "provider_results": collection.get("provider_results", []),
        "top_hot_games_count": len(funnel.get("top_hot_games", [])),
        "selected_topic": funnel.get("selected_topic"),
        "content_package_status": "present" if package else "missing",
        "read_only_surface": True,
        "real_collection_performed": collection.get("real_collection_performed", False),
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(LATEST_REALDATA_OPERATOR_RESULT, artifact)
    return artifact


def readiness(collection: dict[str, Any] | None = None) -> dict[str, Any]:
    collection = collection or collect_providers()
    status = (
        BLOCKED
        if collection["coverage_status"] == BLOCKED
        else "realdata_ready_for_verify"
        if collection["coverage_status"] in {PARTIAL, READY}
        else collection["coverage_status"]
    )
    artifact = {
        "artifact_type": "realdata_readiness",
        "generated_at": _now(),
        "status": status,
        "coverage_status": collection["coverage_status"],
        "successful_provider_count": collection.get("successful_provider_count", 0),
        "coverage_limits": collection.get("coverage_limits", []),
        "real_collection_performed": collection.get("real_collection_performed", False),
        "broad_internet_coverage": False,
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
        "candidate_only": True,
    }
    _write_json(LATEST_REALDATA_READINESS, artifact)
    return artifact


def build_realdata_artifacts() -> dict[str, Any]:
    collection = collect_providers()
    if collection["coverage_status"] == BLOCKED:
        return {
            "provider_contract": json.loads(LATEST_PROVIDER_CONTRACT.read_text(encoding="utf-8")),
            "provider_collection": collection,
            "readiness": readiness(collection),
        }
    fresh = provider_freshness(collection)
    funnel = realdata_funnel(collection)
    package = content_package(funnel)
    operator = operator_result(collection, funnel, package)
    return {
        "provider_contract": json.loads(LATEST_PROVIDER_CONTRACT.read_text(encoding="utf-8")),
        "provider_collection": collection,
        "provider_freshness": fresh,
        "realdata_funnel": funnel,
        "content_package": package,
        "operator_result": operator,
        "readiness": readiness(collection),
    }


def operator_window_html() -> str:
    result = json.loads(LATEST_REALDATA_OPERATOR_RESULT.read_text(encoding="utf-8")) if LATEST_REALDATA_OPERATOR_RESULT.exists() else {}
    ready = json.loads(LATEST_REALDATA_READINESS.read_text(encoding="utf-8")) if LATEST_REALDATA_READINESS.exists() else {}
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko REALDATA</title></head>"
        "<body><h1>REALDATA Provider Coverage</h1>"
        f"<p>Coverage status: {ready.get('coverage_status', result.get('coverage_status', 'missing'))}</p>"
        f"<p>Real collection performed: {str(ready.get('real_collection_performed', False)).lower()}</p>"
        f"<p>Publishing performed: {str(ready.get('publishing_performed', False)).lower()}</p>"
        "<p>Read-only surface. No crawler, scrape, raw source retention, upload, deploy, or publishing path is active.</p>"
        "</body></html>"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run REALDATA multi-provider pipeline.")
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    result = build_realdata_artifacts() if args.write_artifacts else operator_result()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
