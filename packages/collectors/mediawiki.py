import hashlib
import re
from html import unescape
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from packages.collectors.base import ConnectorSearchResult, DisabledConnectorError
from packages.shared.config import get_settings


class MediaWikiConnector:
    name = "mediawiki"
    source_type = "mediawiki"
    source_id_prefix = "mediawiki"
    max_results = 10
    max_snippet_chars = 500

    def __init__(
        self,
        api_url: str = "https://www.pcgamingwiki.com/w/api.php",
        http_get: Callable[[str, dict[str, str], float], dict[str, Any]] | None = None,
    ) -> None:
        self.api_url = api_url
        self.http_get = http_get or self._default_http_get

    def _ensure_enabled(self) -> None:
        if not get_settings().enable_real_connectors:
            raise DisabledConnectorError("Real connectors are disabled by default. Set PIKO_ENABLE_REAL_CONNECTORS=true to opt in.")

    def _default_http_get(self, url: str, headers: dict[str, str], timeout: float) -> dict[str, Any]:
        request = Request(url, headers=headers)
        with urlopen(request, timeout=timeout) as response:
            import json

            return json.loads(response.read().decode("utf-8"))

    def search(self, query: str, limit: int = 5) -> list[ConnectorSearchResult]:
        self._ensure_enabled()
        settings = get_settings()
        safe_limit = max(1, min(limit, self.max_results))
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": str(safe_limit),
        }
        payload = self.http_get(
            f"{self.api_url}?{urlencode(params)}",
            {"User-Agent": settings.connector_user_agent},
            settings.connector_timeout_seconds,
        )
        return [self.normalize(item) for item in payload.get("query", {}).get("search", [])[:safe_limit]]

    def fetch(self, url: str) -> ConnectorSearchResult:
        self._ensure_enabled()
        return ConnectorSearchResult(
            source_id=f"{self.source_id_prefix}_{hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]}",
            source_type=self.source_type,
            url=url,
            title=url.rsplit("/", 1)[-1],
            trust_tier="reference",
            metadata={"fetched": False, "reason": "Fetch body is reserved for a later source-policy round."},
        )

    def normalize(self, item: dict[str, Any]) -> ConnectorSearchResult:
        page_id = str(item.get("pageid", hashlib.sha1(str(item).encode("utf-8")).hexdigest()[:12]))
        title = str(item.get("title", "Untitled"))
        snippet = self._clean_snippet(str(item.get("snippet", "")))
        return ConnectorSearchResult(
            source_id=f"{self.source_id_prefix}_{page_id}",
            source_type=self.source_type,
            url=f"{self.api_url}?curid={page_id}",
            title=title,
            snippet=snippet,
            trust_tier="reference",
            clean_text=snippet,
            metadata={"pageid": page_id, "raw_text_included": False},
        )

    def _clean_snippet(self, snippet: str) -> str:
        text = re.sub(r"<[^>]+>", "", unescape(snippet))
        text = re.sub(r"\s+", " ", text).strip()
        return text[: self.max_snippet_chars]
