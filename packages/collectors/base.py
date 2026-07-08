from datetime import datetime, timezone
from typing import Protocol

from pydantic import BaseModel, Field


class ConnectorSearchResult(BaseModel):
    source_id: str
    source_type: str
    url: str
    title: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    snippet: str = ""
    trust_tier: str = "unknown"
    raw_text: str | None = None
    clean_text: str | None = None
    metadata: dict = Field(default_factory=dict)


class SourceConnector(Protocol):
    name: str

    def search(self, query: str, limit: int = 5) -> list[ConnectorSearchResult]:
        ...

    def fetch(self, url: str) -> ConnectorSearchResult:
        ...

    def normalize(self, item: dict) -> ConnectorSearchResult:
        ...


class DisabledConnectorError(RuntimeError):
    pass
