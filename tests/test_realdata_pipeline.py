import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.realdata.pipeline import (
    BLOCKED,
    PARTIAL,
    READY,
    LATEST_PROVIDER_COLLECTION,
    LATEST_PROVIDER_CONTRACT,
    build_realdata_artifacts,
    collect_providers,
    provider_contract,
)
from packages.shared.config import get_settings


client = TestClient(app)


def _clear_env(monkeypatch) -> None:
    for name in [
        "PIKO_ENABLE_DISCOVERY_REAL_SOURCE",
        "PIKO_LIVE_DISCOVERY_TEST",
        "PIKO_STEAM_DISCOVERY_URL",
        "PIKO_REDDIT_DISCOVERY_URL",
        "PIKO_SERP_DISCOVERY_URL",
        "PIKO_JP_COMMUNITY_DISCOVERY_URL",
        "PIKO_KR_COMMUNITY_DISCOVERY_URL",
    ]:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()


def test_realdata_provider_contract_lists_all_providers_and_forbidden_fields() -> None:
    contract = provider_contract()
    providers = {item["provider_id"] for item in contract["providers"]}
    assert providers == {"steam", "reddit", "serp_snippet", "jp_community", "kr_community"}
    prohibited = set(contract["providers"][0]["prohibited_fields"])
    assert {"raw_text", "body", "selftext", "full_comments", "authorization", "api_key"}.issubset(prohibited)
    assert contract["crawler_allowed"] is False
    assert contract["raw_full_source_retention_allowed"] is False
    assert Path(LATEST_PROVIDER_CONTRACT).exists()


def test_realdata_missing_provider_endpoints_blocks(monkeypatch) -> None:
    _clear_env(monkeypatch)
    result = build_realdata_artifacts()
    assert result["provider_collection"]["coverage_status"] == BLOCKED
    assert result["provider_collection"]["real_collection_performed"] is False
    assert result["readiness"]["status"] == BLOCKED
    assert json.loads(Path(LATEST_PROVIDER_COLLECTION).read_text(encoding="utf-8"))["hot_games"] == []


def test_realdata_partial_and_ready_coverage_with_mock_connectors(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_STEAM_DISCOVERY_URL", "https://provider.example/steam")
    get_settings.cache_clear()

    def fake_collect(self, query="", limit_per_source=5):
        from packages.discovery.real_market import normalize_real_market_payloads

        result = normalize_real_market_payloads(
            {
                self.source_category: {
                    "hot_games": [{"game_id": "g1", "game_name": "Game One", "source_category": self.source_category, "source_url": "https://example.invalid/g", "velocity": 40}],
                    "player_questions": [{"question_id": "q1", "game_id": "g1", "game_name": "Game One", "question_text": "Where is the save file?", "source_category": self.source_category, "source_url": "https://example.invalid/q", "source_title": "Q", "answer_maturity": "answered", "engagement_count": 99, "snippet": "short"}],
                }
            }
        )
        result.real_collection_performed = True
        return result

    monkeypatch.setattr("packages.collectors.real_market.RealMarketConnectorAdapter.collect", fake_collect)
    partial = collect_providers()
    assert partial["coverage_status"] == PARTIAL
    assert partial["real_collection_performed"] is True

    monkeypatch.setenv("PIKO_REDDIT_DISCOVERY_URL", "https://provider.example/reddit")
    get_settings.cache_clear()
    ready = collect_providers()
    assert ready["coverage_status"] == READY
    assert ready["successful_provider_count"] == 2


def test_realdata_api_window_default_blocked(monkeypatch) -> None:
    _clear_env(monkeypatch)
    result = client.get("/realdata/result")
    window = client.get("/realdata/window")
    assert result.status_code == 200
    assert result.json()["provider_collection"]["coverage_status"] == BLOCKED
    assert result.json()["provider_collection"]["real_collection_performed"] is False
    assert window.status_code == 200
    assert "No crawler, scrape, raw source retention" in window.text
