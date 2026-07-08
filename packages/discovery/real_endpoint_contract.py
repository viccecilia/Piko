import json
from pathlib import Path
from typing import Any

from packages.discovery.real_market import (
    MAX_SNIPPET_CHARS,
    REAL_MARKET_PROHIBITED_RETENTION,
    REAL_MARKET_RETAINED_FIELDS,
    REAL_MARKET_SOURCE_CATEGORIES,
    RealMarketConfigError,
    RealMarketNormalizationResult,
    RealMarketSourceCategory,
    normalize_real_market_payloads,
)

APPROVED_ENDPOINT_REQUIRED_ROOT_FIELDS = ["games", "questions", "source", "generated_at"]
APPROVED_ENDPOINT_REQUIRED_SOURCE_FIELDS = ["source_id", "source_type", "source_category", "endpoint_type"]
APPROVED_ENDPOINT_REQUIRED_GAME_FIELDS = ["game_id", "game_name", "source_category", "source_url"]
APPROVED_ENDPOINT_REQUIRED_QUESTION_FIELDS = [
    "question_id",
    "game_id",
    "game_name",
    "question_text",
    "source_category",
    "source_url",
    "source_title",
    "snippet",
]
APPROVED_ENDPOINT_RETAINED_FIELDS = sorted(
    {
        "games",
        "questions",
        "source",
        "generated_at",
        "metadata",
        "game_id",
        "game_name",
        "source_category",
        "source_url",
        "rank",
        "velocity",
        "update_recency_days",
        "question_id",
        "question_text",
        "source_title",
        "url",
        "language",
        "region",
        "engagement_count",
        "reply_count",
        "growth_24h",
        "answer_maturity",
        "conflict_count",
        "risk_level",
        "snippet",
        "tags",
    }
)
APPROVED_ENDPOINT_PROHIBITED_FIELDS = {
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
    "credentials",
    "credential",
    "secret",
    "password",
    "api_key",
    "authorization",
    "access_token",
    "refresh_token",
}
APPROVED_ENDPOINT_FIXTURE_PATH = Path("fixtures/real_endpoint/approved_market_payload.json")


def approved_endpoint_contract() -> dict[str, Any]:
    return {
        "root_fields": APPROVED_ENDPOINT_REQUIRED_ROOT_FIELDS,
        "source_fields": APPROVED_ENDPOINT_REQUIRED_SOURCE_FIELDS,
        "hot_game_fields": APPROVED_ENDPOINT_REQUIRED_GAME_FIELDS,
        "player_question_fields": APPROVED_ENDPOINT_REQUIRED_QUESTION_FIELDS,
        "retained_fields": APPROVED_ENDPOINT_RETAINED_FIELDS,
        "prohibited_fields": sorted(APPROVED_ENDPOINT_PROHIBITED_FIELDS),
        "max_snippet_chars": MAX_SNIPPET_CHARS,
        "approved_endpoint_types": ["json"],
        "rejected_endpoint_types": ["html", "raw_body", "raw_page", "rss_full_text"],
        "html_pages_approved": False,
        "raw_body_endpoints_approved": False,
        "candidate_only": True,
    }


def _walk_keys(value: Any, path: str = "$") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}"
            found.append((str(key), item_path))
            found.extend(_walk_keys(item, item_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_walk_keys(item, f"{path}[{index}]"))
    return found


def validate_approved_endpoint_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise RealMarketConfigError("Approved endpoint payload root must be a JSON object.")
    missing_root = [field for field in APPROVED_ENDPOINT_REQUIRED_ROOT_FIELDS if field not in payload]
    if missing_root:
        raise RealMarketConfigError(f"Approved endpoint payload missing root fields: {', '.join(missing_root)}.")
    if not isinstance(payload.get("games"), list) or not isinstance(payload.get("questions"), list):
        raise RealMarketConfigError("Approved endpoint payload games and questions must be lists.")
    source = payload.get("source")
    if not isinstance(source, dict):
        raise RealMarketConfigError("Approved endpoint source must be an object.")
    missing_source = [field for field in APPROVED_ENDPOINT_REQUIRED_SOURCE_FIELDS if field not in source]
    if missing_source:
        raise RealMarketConfigError(f"Approved endpoint source missing fields: {', '.join(missing_source)}.")
    if source.get("endpoint_type") != "json":
        raise RealMarketConfigError("Only approved JSON endpoints are supported; HTML/raw body endpoints are rejected.")
    source_category = source.get("source_category")
    if source_category not in REAL_MARKET_SOURCE_CATEGORIES:
        raise RealMarketConfigError(f"Unsupported source_category: {source_category}.")
    prohibited_paths = [
        path
        for key, path in _walk_keys(payload)
        if key.lower() in APPROVED_ENDPOINT_PROHIBITED_FIELDS
    ]
    if prohibited_paths:
        raise RealMarketConfigError(f"Approved endpoint payload contains prohibited fields: {', '.join(prohibited_paths)}.")
    return {
        "status": "valid",
        "source_category": source_category,
        "game_count": len(payload["games"]),
        "question_count": len(payload["questions"]),
        "retained_fields": APPROVED_ENDPOINT_RETAINED_FIELDS,
        "prohibited_fields": sorted(APPROVED_ENDPOINT_PROHIBITED_FIELDS),
    }


def _category_for(item: dict[str, Any], fallback: RealMarketSourceCategory) -> RealMarketSourceCategory:
    category = item.get("source_category") or fallback
    if category not in REAL_MARKET_SOURCE_CATEGORIES:
        return fallback
    return category


def normalize_approved_endpoint_payload(payload: dict[str, Any]) -> RealMarketNormalizationResult:
    validated = validate_approved_endpoint_payload(payload)
    fallback = validated["source_category"]
    grouped: dict[RealMarketSourceCategory, dict[str, list[dict[str, Any]]]] = {
        category: {"hot_games": [], "player_questions": []} for category in REAL_MARKET_SOURCE_CATEGORIES
    }
    for game in payload["games"]:
        if isinstance(game, dict):
            grouped[_category_for(game, fallback)]["hot_games"].append(game)
    for question in payload["questions"]:
        if isinstance(question, dict):
            grouped[_category_for(question, fallback)]["player_questions"].append(question)
    return normalize_real_market_payloads(grouped)


def load_approved_endpoint_fixture(path: Path = APPROVED_ENDPOINT_FIXTURE_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def approved_endpoint_safety_flags() -> dict[str, bool]:
    return {
        "default_network_disabled": True,
        "crawler_used": False,
        "html_scrape_allowed": False,
        "raw_response_body_saved": False,
        "publishing_performed": False,
        "deploy_performed": False,
        "llm_called": False,
        "translation_api_called": False,
        "candidate_only": True,
    }
