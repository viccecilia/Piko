import os

import pytest
from urllib.parse import parse_qs, urlparse

from packages.collectors.base import ConnectorSearchResult, DisabledConnectorError
from packages.collectors.dedup import assign_trust_tier, deduplicate_sources
from packages.collectors.fixture_connector import LocalFixtureConnector
from packages.collectors.mediawiki import MediaWikiConnector
from packages.collectors.pcgamingwiki import PCGamingWikiConnector
from packages.shared.config import get_settings
from packages.shared.schemas import SourceReference


def test_default_config_disables_real_connectors() -> None:
    assert get_settings().enable_real_connectors is False
    assert get_settings().live_connector_test is False
    with pytest.raises(DisabledConnectorError):
        MediaWikiConnector().search("Example Game")


def test_local_fixture_connector_implements_protocol_shape() -> None:
    results = LocalFixtureConnector().search("crash on startup")

    assert results
    assert all(result.url.startswith("https://example.invalid/") for result in results)
    assert all(result.trust_tier != "unknown" for result in results)


def test_mediawiki_connector_uses_mocked_http_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "true")
    get_settings.cache_clear()

    def fake_http_get(url: str, headers: dict[str, str], timeout: float) -> dict:
        assert "action=query" in url
        assert "User-Agent" in headers
        return {"query": {"search": [{"pageid": 123, "title": "Example Game", "snippet": "<span>Launch</span> issue notes"}]}}

    try:
        results = MediaWikiConnector(http_get=fake_http_get).search("Example Game", limit=1)
        assert results[0].source_id == "mediawiki_123"
        assert results[0].trust_tier == "reference"
        assert results[0].retrieved_at is not None
        assert results[0].snippet == "Launch issue notes"
    finally:
        monkeypatch.delenv("PIKO_ENABLE_REAL_CONNECTORS", raising=False)
        get_settings.cache_clear()


def test_mediawiki_connector_applies_safety_bounds_and_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "true")
    get_settings.cache_clear()

    observed: dict = {}

    def fake_http_get(url: str, headers: dict[str, str], timeout: float) -> dict:
        observed["params"] = parse_qs(urlparse(url).query)
        observed["headers"] = headers
        observed["timeout"] = timeout
        return {
            "query": {
                "search": [
                    {"pageid": index, "title": f"Example Game {index}", "snippet": "Short source snippet"}
                    for index in range(20)
                ]
            }
        }

    try:
        results = MediaWikiConnector(http_get=fake_http_get).search("Example Game", limit=50)
        assert observed["params"]["srlimit"] == ["10"]
        assert observed["headers"]["User-Agent"] == get_settings().connector_user_agent
        assert observed["timeout"] == get_settings().connector_timeout_seconds
        assert len(results) == 10
        assert all(result.raw_text is None for result in results)
        assert all(result.metadata["raw_text_included"] is False for result in results)
    finally:
        monkeypatch.delenv("PIKO_ENABLE_REAL_CONNECTORS", raising=False)
        get_settings.cache_clear()


def test_pcgamingwiki_connector_normalizes_to_source_reference_shape(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "true")
    get_settings.cache_clear()

    def fake_http_get(url: str, headers: dict[str, str], timeout: float) -> dict:
        return {"query": {"search": [{"pageid": 456, "title": "Example Game", "snippet": "Settings and launch notes"}]}}

    try:
        result = PCGamingWikiConnector(http_get=fake_http_get).search("Example Game", limit=1)[0]
        source = SourceReference.model_validate(result.model_dump(include={"source_id", "source_type", "url", "title", "retrieved_at", "trust_tier"}))

        assert source.source_id == "pcgamingwiki_456"
        assert source.source_type == "pcgamingwiki"
        assert source.url.endswith("?curid=456")
        assert source.title == "Example Game"
        assert source.trust_tier == "reference"
        assert source.retrieved_at is not None
        assert result.clean_text == "Settings and launch notes"
        assert result.raw_text is None
    finally:
        monkeypatch.delenv("PIKO_ENABLE_REAL_CONNECTORS", raising=False)
        get_settings.cache_clear()


@pytest.mark.skipif(
    os.getenv("PIKO_ENABLE_REAL_CONNECTORS") != "true" or os.getenv("PIKO_LIVE_CONNECTOR_TEST") != "true",
    reason="Live connector smoke requires explicit PIKO_ENABLE_REAL_CONNECTORS=true and PIKO_LIVE_CONNECTOR_TEST=true.",
)
def test_live_pcgamingwiki_mediawiki_smoke() -> None:
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.enable_real_connectors is True
    assert settings.live_connector_test is True
    assert settings.connector_timeout_seconds > 0
    assert settings.connector_user_agent.startswith("PikoBot/")

    results = PCGamingWikiConnector().search("Hades", limit=3)

    assert 1 <= len(results) <= 3
    for result in results:
        source = SourceReference.model_validate(result.model_dump(include={"source_id", "source_type", "url", "title", "retrieved_at", "trust_tier"}))
        assert source.source_id.startswith("pcgamingwiki_")
        assert source.source_type == "pcgamingwiki"
        assert source.url
        assert source.title
        assert source.retrieved_at is not None
        assert source.trust_tier == "reference"
        assert result.raw_text is None
        assert len(result.snippet) <= 500
        assert result.metadata["raw_text_included"] is False


def test_dedup_collapses_duplicate_sources_and_assigns_trust() -> None:
    items = [
        ConnectorSearchResult(source_id="a", source_type="steam_discussion", url="https://example.invalid/a", title="Same", clean_text="same"),
        ConnectorSearchResult(source_id="b", source_type="steam_discussion", url="https://example.invalid/a", title="Same", clean_text="same"),
    ]

    deduped = deduplicate_sources(items)
    assert len(deduped) == 1
    assert deduped[0].trust_tier == "community"
    assert assign_trust_tier("official_notes") == "official"
