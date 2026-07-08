import argparse
import json
from typing import Any

from packages.discovery.real_market import bounded_real_market_limits, endpoint_config, real_market_policy
from packages.discovery.real_source import (
    DiscoveryHTTPClient,
    DiscoveryLiveSmokeSkipped,
    DiscoveryRealSourceConfigurationError,
    DiscoveryRealSourceDisabledError,
    RealMarketDiscoverySource,
)
from packages.shared.config import get_settings


def real_market_live_smoke_contract() -> dict[str, Any]:
    settings = get_settings()
    endpoints = endpoint_config(settings)
    configured = {name: bool(url) for name, url in endpoints.items()}
    enabled = settings.enable_discovery_real_source and settings.live_discovery_test
    missing_reason = None
    if not enabled:
        missing_reason = (
            "Skipped unless PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and "
            "PIKO_LIVE_DISCOVERY_TEST=true."
        )
    elif not any(configured.values()):
        missing_reason = "Skipped because no real-market endpoint URL is configured."
    return {
        "status": "available",
        "enabled": enabled and any(configured.values()),
        "skip_reason": missing_reason,
        "required_flags": [
            "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true",
            "PIKO_LIVE_DISCOVERY_TEST=true",
        ],
        "configured_endpoints": configured,
        "limits": bounded_real_market_limits(max_sources=2, max_records_per_source=3),
        "timeout_seconds": settings.connector_timeout_seconds,
        "user_agent": settings.connector_user_agent,
        "retained_fields": [
            "source_name",
            "source_type",
            "source_region",
            "games",
            "questions",
            "title",
            "url",
            "snippet",
            "engagement_count",
            "reply_count",
            "growth_24h",
        ],
        "prohibited_retention": [
            "raw_text",
            "body",
            "selftext",
            "content",
            "full_comments",
            "raw_page_text",
            "full live response body",
        ],
        "policy": real_market_policy(settings),
        "real_collection_performed": False,
        "publishing_performed": False,
    }


def _bounded_summary(result: dict[str, Any]) -> dict[str, Any]:
    games = list(result.get("games") or [])[:3]
    questions = list(result.get("questions") or [])[:3]
    return {
        "status": result.get("status"),
        "mode": result.get("mode"),
        "sources": list(result.get("sources") or [])[:2],
        "game_count": len(result.get("games") or []),
        "question_count": len(result.get("questions") or []),
        "sample_games": [
            {
                "game_id": item.get("game_id"),
                "game_name": item.get("game_name"),
                "heat_score": item.get("heat_score"),
                "region_signals": item.get("region_signals"),
            }
            for item in games
        ],
        "sample_questions": [
            {
                "question_id": item.get("question_id"),
                "game_name": item.get("game_name"),
                "question_text": item.get("question_text"),
                "source_type": item.get("source_type"),
                "source_region": item.get("source_region"),
                "snippet": item.get("snippet"),
                "engagement_count": item.get("engagement_count"),
                "reply_count": item.get("reply_count"),
            }
            for item in questions
        ],
        "real_collection_performed": bool(result.get("real_collection_performed")),
        "publishing_performed": False,
        "full_response_body_saved": False,
    }


def run_real_market_live_smoke(
    query: str = "Stardew Valley",
    limit_per_source: int = 3,
    client: DiscoveryHTTPClient | None = None,
) -> dict[str, Any]:
    contract = real_market_live_smoke_contract()
    if not contract["enabled"]:
        raise DiscoveryLiveSmokeSkipped(str(contract["skip_reason"]))
    bounded_limit = min(max(limit_per_source, 1), int(contract["limits"]["max_records_per_source"]))
    try:
        result = RealMarketDiscoverySource.from_settings(client=client).collect(
            query=query,
            limit_per_source=bounded_limit,
        )
    except DiscoveryRealSourceDisabledError as exc:
        raise DiscoveryLiveSmokeSkipped(str(exc)) from exc
    except DiscoveryRealSourceConfigurationError as exc:
        raise DiscoveryLiveSmokeSkipped(str(exc)) from exc
    summary = _bounded_summary(result)
    summary["contract"] = {
        "limits": contract["limits"],
        "timeout_seconds": contract["timeout_seconds"],
        "configured_endpoints": contract["configured_endpoints"],
    }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a bounded opt-in Piko real-market live smoke.")
    parser.add_argument("--query", default="Stardew Valley")
    parser.add_argument("--limit-per-source", type=int, default=3)
    args = parser.parse_args()
    try:
        result = run_real_market_live_smoke(args.query, args.limit_per_source)
    except DiscoveryLiveSmokeSkipped as exc:
        result = {
            "status": "skipped",
            "reason": str(exc),
            "contract": real_market_live_smoke_contract(),
            "real_collection_performed": False,
            "publishing_performed": False,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
