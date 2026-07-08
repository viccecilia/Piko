from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from packages.shared.config import Settings, get_settings
from packages.shared.schemas import GameHeatSignal, PlayerQuestionSignal

RealMarketSourceCategory = Literal["steam", "reddit", "jp_community", "kr_community", "serp_snippet"]

REAL_MARKET_SOURCE_CATEGORIES: list[RealMarketSourceCategory] = [
    "steam",
    "reddit",
    "jp_community",
    "kr_community",
    "serp_snippet",
]

REAL_MARKET_ENDPOINT_ENV_VARS: dict[RealMarketSourceCategory, str] = {
    "steam": "PIKO_STEAM_DISCOVERY_URL",
    "reddit": "PIKO_REDDIT_DISCOVERY_URL",
    "jp_community": "PIKO_JP_COMMUNITY_DISCOVERY_URL",
    "kr_community": "PIKO_KR_COMMUNITY_DISCOVERY_URL",
    "serp_snippet": "PIKO_SERP_DISCOVERY_URL",
}

REAL_MARKET_REQUIRED_HOT_GAME_FIELDS = [
    "game_id",
    "game_name",
    "source_category",
    "source_url",
    "observed_at",
    "rank",
    "velocity",
    "region",
]

REAL_MARKET_REQUIRED_PLAYER_QUESTION_FIELDS = [
    "question_id",
    "game_id",
    "game_name",
    "question_text",
    "source_category",
    "source_url",
    "source_title",
    "observed_at",
    "engagement_count",
    "reply_count",
    "duplicate_count",
    "answer_maturity",
    "conflict_count",
    "snippet",
]

REAL_MARKET_RETAINED_FIELDS: dict[RealMarketSourceCategory, list[str]] = {
    category: [
        "source_category",
        "source_title",
        "source_url",
        "observed_at",
        "game_id",
        "game_name",
        "rank",
        "velocity",
        "region",
        "language",
        "question_text",
        "engagement_count",
        "reply_count",
        "duplicate_count",
        "answer_maturity",
        "conflict_count",
        "short_snippet",
        "tags",
        "metadata_summary",
    ]
    for category in REAL_MARKET_SOURCE_CATEGORIES
}

REAL_MARKET_PROHIBITED_RETENTION = [
    "raw_text",
    "raw source body",
    "full_post",
    "full posts",
    "full_page",
    "full pages",
    "full_comments",
    "full comments",
    "raw_page_text",
    "raw page text",
    "body",
    "selftext",
    "content",
    "images",
    "maps",
    "credentials",
    "credential",
    "authorization",
    "api_key",
    "password",
    "access_token",
    "refresh_token",
    "secret",
    "full copied tables",
    "table_html",
]

FORBIDDEN_METADATA_KEYS = {
    "raw_text",
    "body",
    "selftext",
    "content",
    "full_post",
    "full_page",
    "full_comments",
    "raw_page_text",
    "credentials",
    "credential",
    "authorization",
    "api_key",
    "password",
    "access_token",
    "refresh_token",
    "secret",
    "table_html",
}

MAX_SNIPPET_CHARS = 280
MAX_REAL_MARKET_SOURCES = 5
MAX_REAL_MARKET_RECORDS_PER_SOURCE = 20


class RealMarketConfigError(RuntimeError):
    pass


class RealMarketSourceSummary(BaseModel):
    source_category: RealMarketSourceCategory
    endpoint_configured: bool = False
    hot_game_count: int = 0
    player_question_count: int = 0
    retained_fields: list[str] = Field(default_factory=list)


class RealMarketNormalizationResult(BaseModel):
    hot_games: list[GameHeatSignal] = Field(default_factory=list)
    player_questions: list[PlayerQuestionSignal] = Field(default_factory=list)
    source_summary: list[RealMarketSourceSummary] = Field(default_factory=list)
    real_collection_performed: bool = False
    candidate_only: bool = True


def real_market_source_contract() -> dict[str, object]:
    return {
        "source_categories": REAL_MARKET_SOURCE_CATEGORIES,
        "required_hot_game_fields": REAL_MARKET_REQUIRED_HOT_GAME_FIELDS,
        "required_player_question_fields": REAL_MARKET_REQUIRED_PLAYER_QUESTION_FIELDS,
        "retained_fields_by_source": REAL_MARKET_RETAINED_FIELDS,
        "prohibited_retention": REAL_MARKET_PROHIBITED_RETENTION,
        "max_snippet_chars": MAX_SNIPPET_CHARS,
        "candidate_only": True,
    }


def endpoint_config(settings: Settings | None = None) -> dict[RealMarketSourceCategory, str | None]:
    settings = settings or get_settings()
    return {
        "steam": settings.steam_discovery_url,
        "reddit": settings.reddit_discovery_url,
        "jp_community": settings.jp_community_discovery_url,
        "kr_community": settings.kr_community_discovery_url,
        "serp_snippet": settings.serp_discovery_url,
    }


def bounded_real_market_limits(max_sources: int | None = None, max_records_per_source: int | None = None) -> dict[str, int]:
    settings = get_settings()
    requested_sources = settings.real_market_max_sources if max_sources is None else max_sources
    requested_records = settings.real_market_max_records_per_source if max_records_per_source is None else max_records_per_source
    return {
        "max_sources": max(1, min(int(requested_sources), MAX_REAL_MARKET_SOURCES)),
        "max_records_per_source": max(1, min(int(requested_records), MAX_REAL_MARKET_RECORDS_PER_SOURCE)),
    }


def validate_real_market_collection_config(
    source_categories: list[RealMarketSourceCategory] | None = None,
    settings: Settings | None = None,
) -> dict[str, object]:
    settings = settings or get_settings()
    source_categories = source_categories or REAL_MARKET_SOURCE_CATEGORIES
    if not (settings.enable_discovery_real_source and settings.live_discovery_test):
        raise RealMarketConfigError(
            "Real-market discovery requires PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true."
        )
    endpoints = endpoint_config(settings)
    missing = [REAL_MARKET_ENDPOINT_ENV_VARS[category] for category in source_categories if not endpoints.get(category)]
    if missing:
        raise RealMarketConfigError(f"Missing real-market endpoint configuration: {', '.join(missing)}.")
    return {
        "enabled": True,
        "source_categories": source_categories,
        "endpoints": {category: endpoints[category] for category in source_categories},
        "limits": bounded_real_market_limits(),
        "timeout_seconds": settings.connector_timeout_seconds,
        "user_agent": settings.connector_user_agent,
    }


def real_market_policy(settings: Settings | None = None) -> dict[str, object]:
    settings = settings or get_settings()
    endpoints = endpoint_config(settings)
    return {
        "enabled": settings.enable_discovery_real_source and settings.live_discovery_test,
        "required_flags": [
            "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true",
            "PIKO_LIVE_DISCOVERY_TEST=true",
        ],
        "endpoint_env_vars": REAL_MARKET_ENDPOINT_ENV_VARS,
        "configured_endpoints": {category: bool(value) for category, value in endpoints.items()},
        "limits": bounded_real_market_limits(),
        "timeout_seconds": settings.connector_timeout_seconds,
        "user_agent": settings.connector_user_agent,
        "default_offline": True,
    }


def _short_text(value: object, limit: int = MAX_SNIPPET_CHARS) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).split())
    if not text:
        return None
    return text[:limit]


def _int_value(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except Exception:
        return default


def _sanitize_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in payload.items():
        normalized_key = key.lower()
        if normalized_key in FORBIDDEN_METADATA_KEYS:
            continue
        if isinstance(value, str) and len(value) > MAX_SNIPPET_CHARS:
            safe[key] = value[:MAX_SNIPPET_CHARS]
        elif isinstance(value, (str, int, float, bool)) or value is None:
            safe[key] = value
    return safe


def _region_for(category: RealMarketSourceCategory, payload: dict[str, Any]) -> str:
    if payload.get("region"):
        return str(payload["region"])
    return {
        "jp_community": "jp",
        "kr_community": "kr",
        "reddit": "en",
        "steam": "global",
        "serp_snippet": "global",
    }[category]


def normalize_hot_game_record(category: RealMarketSourceCategory, payload: dict[str, Any]) -> GameHeatSignal:
    game_id = str(payload.get("game_id") or payload.get("app_id") or payload.get("id") or "unknown_game")
    game_name = str(payload.get("game_name") or payload.get("title") or payload.get("name") or game_id)
    rank = _int_value(payload.get("rank") or payload.get("steam_player_rank"), 999)
    velocity = _int_value(payload.get("velocity") or payload.get("review_velocity") or payload.get("community_velocity"), 0)
    mentions = _int_value(payload.get("mentions") or payload.get("cross_region_mentions"), 0)
    return GameHeatSignal(
        game_id=game_id,
        game_name=game_name,
        region_signals=[category, _region_for(category, payload)],
        steam_player_rank=rank if category == "steam" else None,
        steam_review_velocity=velocity if category == "steam" else 0,
        community_post_velocity=velocity if category != "steam" else _int_value(payload.get("community_post_velocity"), 0),
        update_recency_days=payload.get("update_recency_days"),
        cross_region_mentions=mentions,
        heat_score=max(0, min(100, _int_value(payload.get("heat_score"), min(100, max(0, velocity + mentions * 5))))),
        reasons=[f"Normalized from {category} metadata; candidate signal only."],
    )


def normalize_player_question_record(category: RealMarketSourceCategory, payload: dict[str, Any]) -> PlayerQuestionSignal:
    question_text = str(payload.get("question_text") or payload.get("title") or payload.get("query") or "Unknown player question")
    snippet = _short_text(payload.get("snippet") or payload.get("summary") or payload.get("excerpt") or question_text)
    answer_maturity = str(payload.get("answer_maturity") or payload.get("answer_status") or "unknown")
    evidence_quality = {
        "answered": 70,
        "accepted": 75,
        "official": 80,
        "partial": 45,
        "conflicting": 55,
        "unanswered": 25,
        "unknown": 20,
    }.get(answer_maturity, 20)
    return PlayerQuestionSignal(
        question_id=str(payload.get("question_id") or payload.get("id") or f"{category}_question"),
        game_id=str(payload.get("game_id") or payload.get("app_id") or "unknown_game"),
        game_name=str(payload.get("game_name") or payload.get("game") or "Unknown Game"),
        question_text=question_text,
        source_type=category,
        source_region=_region_for(category, payload),
        source_title=_short_text(payload.get("source_title") or payload.get("title"), 120),
        language=payload.get("language") or _region_for(category, payload),
        url=payload.get("url") or payload.get("source_url"),
        created_at=_parse_datetime(payload.get("created_at") or payload.get("observed_at")),
        engagement_count=_int_value(payload.get("engagement_count") or payload.get("score") or payload.get("upvotes"), 0),
        reply_count=_int_value(payload.get("reply_count") or payload.get("comments"), 0),
        duplicate_count=max(1, _int_value(payload.get("duplicate_count") or payload.get("mentions"), 1)),
        growth_24h=_int_value(payload.get("growth_24h") or payload.get("velocity"), 0),
        has_accepted_answer=answer_maturity in {"accepted", "official"},
        has_official_answer=answer_maturity == "official",
        answer_conflict_count=_int_value(payload.get("conflict_count"), 0),
        evidence_quality=evidence_quality,
        competition_gap=_int_value(payload.get("competition_gap"), 50),
        piko_value_add_score=_int_value(payload.get("piko_value_add_score"), 50),
        risk_level=payload.get("risk_level") or "low",
        tags=[str(tag) for tag in payload.get("tags", [])][:8],
        metadata=_sanitize_metadata(
            {
                "source_category": category,
                "answer_maturity": answer_maturity,
                "normalized_only": True,
                **payload,
            }
        ),
        snippet=snippet,
    )


def normalize_real_market_payloads(
    payloads_by_source: dict[RealMarketSourceCategory, dict[str, list[dict[str, Any]]]],
) -> RealMarketNormalizationResult:
    hot_games: list[GameHeatSignal] = []
    player_questions: list[PlayerQuestionSignal] = []
    summaries: list[RealMarketSourceSummary] = []
    endpoints = endpoint_config()
    limits = bounded_real_market_limits()
    for category in REAL_MARKET_SOURCE_CATEGORIES[: limits["max_sources"]]:
        payload = payloads_by_source.get(category, {})
        game_payloads = payload.get("hot_games", [])[: limits["max_records_per_source"]]
        question_payloads = payload.get("player_questions", [])[: limits["max_records_per_source"]]
        hot_games.extend(normalize_hot_game_record(category, item) for item in game_payloads)
        player_questions.extend(normalize_player_question_record(category, item) for item in question_payloads)
        summaries.append(
            RealMarketSourceSummary(
                source_category=category,
                endpoint_configured=bool(endpoints.get(category)),
                hot_game_count=len(game_payloads),
                player_question_count=len(question_payloads),
                retained_fields=REAL_MARKET_RETAINED_FIELDS[category],
            )
        )
    return RealMarketNormalizationResult(
        hot_games=hot_games,
        player_questions=player_questions,
        source_summary=summaries,
        real_collection_performed=False,
        candidate_only=True,
    )


def _parse_datetime(value: object) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None
