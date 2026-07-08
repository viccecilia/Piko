import json
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from packages.discovery.real_market import (
    MAX_REAL_MARKET_RECORDS_PER_SOURCE,
    RealMarketConfigError,
    RealMarketNormalizationResult,
    RealMarketSourceCategory,
    endpoint_config,
    normalize_real_market_payloads,
    validate_real_market_collection_config,
)
from packages.shared.config import get_settings

RealMarketHTTPGetter = Callable[[str, dict[str, str], float], dict[str, Any]]


def _default_http_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, Any]:
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except URLError as exc:
        raise RealMarketConfigError(f"Real-market connector request failed: {exc}") from exc
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RealMarketConfigError("Real-market connector endpoint did not return JSON.") from exc
    if not isinstance(payload, dict):
        raise RealMarketConfigError("Real-market connector JSON root must be an object.")
    return payload


def _with_query_params(endpoint: str, query: str, limit: int) -> str:
    separator = "&" if "?" in endpoint else "?"
    return f"{endpoint}{separator}{urlencode({'query': query, 'limit': limit})}"


@dataclass(frozen=True)
class RealMarketConnectorAdapter:
    source_category: RealMarketSourceCategory
    http_get: RealMarketHTTPGetter | None = None

    def collect(self, query: str = "", limit_per_source: int = 10) -> RealMarketNormalizationResult:
        config = validate_real_market_collection_config([self.source_category])
        settings = get_settings()
        endpoints = endpoint_config(settings)
        endpoint = endpoints.get(self.source_category)
        if not endpoint:
            raise RealMarketConfigError(f"Missing endpoint for {self.source_category}.")

        bounded_limit = max(1, min(int(limit_per_source), MAX_REAL_MARKET_RECORDS_PER_SOURCE))
        headers = {
            "Accept": "application/json",
            "User-Agent": str(config["user_agent"]),
        }
        getter = self.http_get or _default_http_get
        payload = getter(
            _with_query_params(endpoint, query, bounded_limit),
            headers,
            float(config["timeout_seconds"]),
        )
        result = normalize_real_market_payloads(
            {
                self.source_category: {
                    "hot_games": list(payload.get("hot_games") or payload.get("games") or [])[:bounded_limit],
                    "player_questions": list(payload.get("player_questions") or payload.get("questions") or [])[
                        :bounded_limit
                    ],
                }
            }
        )
        result.real_collection_performed = True
        return result


class SteamMarketConnector(RealMarketConnectorAdapter):
    def __init__(self, http_get: RealMarketHTTPGetter | None = None) -> None:
        super().__init__("steam", http_get=http_get)


class RedditMarketConnector(RealMarketConnectorAdapter):
    def __init__(self, http_get: RealMarketHTTPGetter | None = None) -> None:
        super().__init__("reddit", http_get=http_get)


class SERPMarketConnector(RealMarketConnectorAdapter):
    def __init__(self, http_get: RealMarketHTTPGetter | None = None) -> None:
        super().__init__("serp_snippet", http_get=http_get)


class JPCommunityMarketConnector(RealMarketConnectorAdapter):
    def __init__(self, http_get: RealMarketHTTPGetter | None = None) -> None:
        super().__init__("jp_community", http_get=http_get)


class KRCommunityMarketConnector(RealMarketConnectorAdapter):
    def __init__(self, http_get: RealMarketHTTPGetter | None = None) -> None:
        super().__init__("kr_community", http_get=http_get)
