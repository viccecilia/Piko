from packages.collectors.base import ConnectorSearchResult
from packages.collectors.local_fixtures import select_local_source_candidates


class LocalFixtureConnector:
    name = "local_fixture"

    def search(self, query: str, limit: int = 5) -> list[ConnectorSearchResult]:
        candidates = select_local_source_candidates("Example Game", query)[:limit]
        return [
            ConnectorSearchResult(
                source_id=item["source_id"],
                source_type=item["source_type"],
                url=item["url"],
                title=item["title"],
                snippet=item["reason"],
                trust_tier=item["trust_tier"],
                clean_text=item["reason"],
                metadata={"platform": item["platform"], "score": item["score"]},
            )
            for item in candidates
        ]

    def fetch(self, url: str) -> ConnectorSearchResult:
        matches = [result for result in self.search("crash on startup", limit=10) if result.url == url]
        if not matches:
            raise ValueError(f"Unknown local fixture URL: {url}")
        return matches[0]

    def normalize(self, item: dict) -> ConnectorSearchResult:
        return ConnectorSearchResult.model_validate(item)

