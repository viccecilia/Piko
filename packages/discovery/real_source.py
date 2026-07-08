import json
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import URLError
from urllib.request import Request, urlopen

from packages.shared.config import get_settings
from packages.shared.schemas import GameHeatSignal, PlayerQuestionSignal

DISCOVERY_REAL_SOURCE_PILOT = {
    "selected_source": "pcgamingwiki_mediawiki",
    "source_type": "wiki_metadata",
    "env_flags": ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true", "PIKO_LIVE_DISCOVERY_TEST=true"],
    "timeout_seconds_setting": "PIKO_CONNECTOR_TIMEOUT_SECONDS",
    "default_timeout_seconds": 5.0,
    "max_result_limit": 3,
    "retained_fields": [
        "question_id",
        "game_id",
        "game_name",
        "question_text",
        "source_type",
        "source_region",
        "source_title",
        "url",
        "engagement_count",
        "reply_count",
        "duplicate_count",
        "growth_24h",
        "evidence_quality",
        "tags",
        "snippet",
        "metadata",
    ],
    "prohibited_retention": ["raw full page text", "full posts", "images", "maps", "copied tables", "credentials"],
}


class DiscoveryRealSourceDisabledError(RuntimeError):
    pass


class DiscoveryLiveSmokeSkipped(RuntimeError):
    pass


class DiscoveryRealSourceConfigurationError(RuntimeError):
    pass


class DiscoveryRealSourceFetchError(RuntimeError):
    pass


class DiscoveryHTTPClient(Protocol):
    def get_json(self, url: str, *, timeout: float, user_agent: str) -> dict[str, Any]:
        ...


class UrllibDiscoveryHTTPClient:
    def get_json(self, url: str, *, timeout: float, user_agent: str) -> dict[str, Any]:
        request = Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
        except URLError as exc:
            raise DiscoveryRealSourceFetchError(f"Failed to fetch discovery source: {exc}") from exc
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise DiscoveryRealSourceFetchError("Discovery source did not return JSON.") from exc
        if not isinstance(payload, dict):
            raise DiscoveryRealSourceFetchError("Discovery source JSON root must be an object.")
        return payload


@dataclass(frozen=True)
class RealDiscoveryEndpoint:
    source_name: str
    source_type: str
    source_region: str
    url: str | None


def _bounded_text(value: object, limit: int = 500) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).split())
    if not text:
        return None
    return text[:limit]


def _bounded_int(value: object, default: int = 0, minimum: int = 0, maximum: int | None = None) -> int:
    try:
        number = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        number = default
    number = max(minimum, number)
    if maximum is not None:
        number = min(maximum, number)
    return number


def _safe_metadata(item: dict[str, Any], source_name: str) -> dict[str, Any]:
    allowed = {
        "thread_id",
        "subreddit",
        "score",
        "upvote_ratio",
        "comment_count",
        "language",
        "community",
        "rank",
        "app_id",
        "platform",
        "answer_url",
        "accepted_answer_id",
    }
    return {
        key: value
        for key, value in item.items()
        if key in allowed and value is not None and key not in {"raw_text", "body", "selftext", "content"}
    } | {"source_name": source_name, "raw_text_included": False}


class RealMarketDiscoverySource:
    def __init__(self, endpoints: list[RealDiscoveryEndpoint], client: DiscoveryHTTPClient | None = None) -> None:
        self.endpoints = endpoints
        self.client = client or UrllibDiscoveryHTTPClient()

    @classmethod
    def from_settings(cls, client: DiscoveryHTTPClient | None = None) -> "RealMarketDiscoverySource":
        settings = get_settings()
        return cls(
            [
                RealDiscoveryEndpoint("steam", "steam_discussion", "global", settings.steam_discovery_url),
                RealDiscoveryEndpoint("reddit", "reddit", "global", settings.reddit_discovery_url),
                RealDiscoveryEndpoint("jp_community", "jp_community", "jp", settings.jp_community_discovery_url),
                RealDiscoveryEndpoint("kr_community", "kr_community", "kr", settings.kr_community_discovery_url),
            ],
            client=client,
        )

    def _assert_enabled(self) -> None:
        settings = get_settings()
        if not (settings.enable_discovery_real_source and settings.live_discovery_test):
            raise DiscoveryRealSourceDisabledError(
                "Broad market discovery requires PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true."
            )

    def _active_endpoints(self) -> list[RealDiscoveryEndpoint]:
        active = [endpoint for endpoint in self.endpoints if endpoint.url]
        if not active:
            raise DiscoveryRealSourceConfigurationError(
                "No real discovery endpoints configured. Set one or more of PIKO_STEAM_DISCOVERY_URL, "
                "PIKO_REDDIT_DISCOVERY_URL, PIKO_JP_COMMUNITY_DISCOVERY_URL, or PIKO_KR_COMMUNITY_DISCOVERY_URL."
            )
        return active

    def collect(self, query: str = "", limit_per_source: int = 10) -> dict[str, object]:
        self._assert_enabled()
        settings = get_settings()
        games: list[GameHeatSignal] = []
        questions: list[PlayerQuestionSignal] = []
        source_summaries: list[dict[str, object]] = []
        bounded_limit = min(max(limit_per_source, 1), 25)

        for endpoint in self._active_endpoints():
            assert endpoint.url is not None
            payload = self.client.get_json(
                endpoint.url,
                timeout=settings.connector_timeout_seconds,
                user_agent=settings.connector_user_agent,
            )
            endpoint_games = [
                self._normalize_game(item, endpoint)
                for item in payload.get("games", [])
                if isinstance(item, dict)
            ][:bounded_limit]
            endpoint_questions = [
                self._normalize_question(item, endpoint, query=query)
                for item in payload.get("questions", [])
                if isinstance(item, dict)
            ][:bounded_limit]
            games.extend(endpoint_games)
            questions.extend(endpoint_questions)
            source_summaries.append(
                {
                    "source_name": endpoint.source_name,
                    "source_type": endpoint.source_type,
                    "source_region": endpoint.source_region,
                    "games": len(endpoint_games),
                    "questions": len(endpoint_questions),
                }
            )

        return {
            "status": "completed",
            "mode": "real-source",
            "sources": source_summaries,
            "games": [game.model_dump(mode="json") for game in games],
            "questions": [question.model_dump(mode="json") for question in questions],
            "retained_fields": DISCOVERY_REAL_SOURCE_PILOT["retained_fields"],
            "real_collection_performed": True,
            "publishing_performed": False,
        }

    def _normalize_game(self, item: dict[str, Any], endpoint: RealDiscoveryEndpoint) -> GameHeatSignal:
        game_id = _bounded_text(item.get("game_id") or item.get("app_id") or item.get("slug") or item.get("game_name"), 120)
        game_name = _bounded_text(item.get("game_name") or item.get("name") or game_id, 160)
        return GameHeatSignal(
            game_id=(game_id or "unknown_game").replace(" ", "_").lower(),
            game_name=game_name or "Unknown Game",
            region_signals=list(dict.fromkeys(["steam" if endpoint.source_name == "steam" else endpoint.source_region, endpoint.source_region])),
            steam_player_rank=_bounded_int(item.get("steam_player_rank") or item.get("rank"), default=999, minimum=1)
            if endpoint.source_name == "steam"
            else item.get("steam_player_rank"),
            steam_review_velocity=_bounded_int(item.get("steam_review_velocity"), maximum=100),
            community_post_velocity=_bounded_int(item.get("community_post_velocity") or item.get("post_velocity"), maximum=100),
            update_recency_days=_bounded_int(item.get("update_recency_days"), minimum=0)
            if item.get("update_recency_days") is not None
            else None,
            cross_region_mentions=_bounded_int(item.get("cross_region_mentions"), maximum=100),
        )

    def _normalize_question(self, item: dict[str, Any], endpoint: RealDiscoveryEndpoint, query: str = "") -> PlayerQuestionSignal:
        question_text = _bounded_text(item.get("question_text") or item.get("title") or item.get("query") or query, 300)
        game_name = _bounded_text(item.get("game_name") or item.get("name") or query or "Unknown Game", 160)
        game_id = _bounded_text(item.get("game_id") or item.get("app_id") or game_name, 120)
        source_region = _bounded_text(item.get("source_region") or item.get("region") or endpoint.source_region, 40)
        return PlayerQuestionSignal(
            question_id=_bounded_text(item.get("question_id") or item.get("thread_id") or item.get("id"), 160)
            or f"{endpoint.source_name}_question",
            game_id=(game_id or "unknown_game").replace(" ", "_").lower(),
            game_name=game_name or "Unknown Game",
            question_text=question_text or "Unknown player question",
            source_type=_bounded_text(item.get("source_type") or endpoint.source_type, 80) or endpoint.source_type,
            source_region=source_region or endpoint.source_region,
            source_title=_bounded_text(item.get("source_title") or item.get("title"), 180),
            language=_bounded_text(item.get("language") or source_region, 40),
            url=_bounded_text(item.get("url") or item.get("permalink"), 500),
            engagement_count=_bounded_int(item.get("engagement_count") or item.get("score") or item.get("upvotes")),
            reply_count=_bounded_int(item.get("reply_count") or item.get("comment_count") or item.get("num_comments")),
            duplicate_count=_bounded_int(item.get("duplicate_count"), default=1, minimum=1),
            growth_24h=_bounded_int(item.get("growth_24h") or item.get("velocity_24h"), maximum=100),
            has_accepted_answer=bool(item.get("has_accepted_answer")),
            has_official_answer=bool(item.get("has_official_answer")),
            answer_conflict_count=_bounded_int(item.get("answer_conflict_count"), maximum=100),
            evidence_quality=_bounded_int(item.get("evidence_quality"), maximum=100),
            competition_gap=_bounded_int(item.get("competition_gap"), default=50, maximum=100),
            piko_value_add_score=_bounded_int(item.get("piko_value_add_score"), default=50, maximum=100),
            risk_level=item.get("risk_level") if item.get("risk_level") in {"low", "medium", "high"} else "low",
            tags=[_bounded_text(tag, 40) or "" for tag in item.get("tags", []) if _bounded_text(tag, 40)][:12],
            snippet=_bounded_text(item.get("snippet") or item.get("excerpt") or item.get("summary"), 500),
            metadata=_safe_metadata(item, endpoint.source_name),
        )


class FixtureDiscoverySource:
    source_name = "fixture_discovery_source"

    def search_questions(self, query: str, limit: int = 5) -> list[PlayerQuestionSignal]:
        settings = get_settings()
        if not (settings.enable_discovery_real_source and settings.live_discovery_test):
            raise DiscoveryRealSourceDisabledError(
                "Discovery real-source search requires PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true."
            )
        bounded_limit = min(limit, DISCOVERY_REAL_SOURCE_PILOT["max_result_limit"])
        return [
            PlayerQuestionSignal(
                question_id="live_fixture_question_001",
                game_id="demo_game",
                game_name=query,
                question_text=f"{query} save location question from opt-in discovery fixture",
                source_type="pcgamingwiki_mediawiki",
                source_region="global",
                source_title="Opt-in discovery fixture",
                engagement_count=1,
                reply_count=0,
                duplicate_count=1,
                growth_24h=0,
                evidence_quality=50,
                tags=["save", "location"],
                snippet="Short metadata-only discovery fixture; no raw page body stored.",
                metadata={"raw_text_included": False, "live_smoke_fixture": True},
            )
        ][:bounded_limit]


def discovery_live_smoke_contract() -> dict[str, object]:
    settings = get_settings()
    enabled = settings.enable_discovery_real_source and settings.live_discovery_test
    return {
        **DISCOVERY_REAL_SOURCE_PILOT,
        "enabled": enabled,
        "skip_reason": None
        if enabled
        else "Skipped unless PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true and PIKO_LIVE_DISCOVERY_TEST=true.",
        "timeout_seconds": settings.connector_timeout_seconds,
        "broad_market_sources": [
            {
                "source_name": "steam",
                "source_type": "steam_discussion",
                "configured": bool(settings.steam_discovery_url),
            },
            {
                "source_name": "reddit",
                "source_type": "reddit",
                "configured": bool(settings.reddit_discovery_url),
            },
            {
                "source_name": "jp_community",
                "source_type": "jp_community",
                "configured": bool(settings.jp_community_discovery_url),
            },
            {
                "source_name": "kr_community",
                "source_type": "kr_community",
                "configured": bool(settings.kr_community_discovery_url),
            },
        ],
        "real_collection_performed": False,
        "publishing_performed": False,
    }


def run_discovery_live_smoke(query: str = "Stardew Valley", limit: int = 3) -> dict[str, object]:
    contract = discovery_live_smoke_contract()
    if not contract["enabled"]:
        raise DiscoveryLiveSmokeSkipped(str(contract["skip_reason"]))
    records = FixtureDiscoverySource().search_questions(query, limit=min(limit, int(contract["max_result_limit"])))
    return {
        "status": "completed",
        "selected_source": contract["selected_source"],
        "result_limit": len(records),
        "records": [record.model_dump(mode="json") for record in records],
        "retained_fields": contract["retained_fields"],
        "real_collection_performed": False,
        "publishing_performed": False,
    }
