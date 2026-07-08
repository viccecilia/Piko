import json
from pathlib import Path

from packages.provider_live.pipeline import (
    DEPLOY_READY_PENDING_HOST,
    LATEST_ENDPOINT_STATUS,
    PROVIDER_LIVE_READY,
    build_provider_live_artifacts,
    endpoint_status,
    provider_package,
    provider_package_contract,
    validate_provider_endpoint,
)
from packages.shared.config import get_settings


def _clear_env(monkeypatch) -> None:
    for name in [
        "PIKO_ENABLE_DISCOVERY_REAL_SOURCE",
        "PIKO_LIVE_DISCOVERY_TEST",
        "PIKO_SERP_DISCOVERY_URL",
        "PIKO_REDDIT_DISCOVERY_URL",
        "PIKO_STEAM_DISCOVERY_URL",
    ]:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()


def test_provider_live_contract_and_packages_are_safe() -> None:
    contract = provider_package_contract()
    providers = {item["provider_id"] for item in contract["providers"]}
    assert providers == {"serp_snippet", "reddit", "steam"}
    assert contract["default_network_disabled"] is True
    assert contract["crawler_allowed"] is False
    assert "raw_text" in contract["retention_policy"]["prohibited_fields"]

    for provider in ["serp_snippet", "reddit", "steam"]:
        package = provider_package(provider)  # type: ignore[arg-type]
        keys = set()

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    keys.add(key.lower())
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(package)
        assert "raw_text" not in keys
        assert "selftext" not in keys
        assert package["metadata"]["candidate_only"] is True
        assert package["metadata"]["broad_internet_coverage"] is False


def test_provider_live_blocks_without_provider_endpoint(monkeypatch) -> None:
    _clear_env(monkeypatch)
    result = build_provider_live_artifacts()
    assert result["endpoint_status"]["provider_live_status"] == DEPLOY_READY_PENDING_HOST
    assert result["endpoint_status"]["real_collection_performed"] is False
    assert result["readiness"]["partial_provider_endpoint_ready"] is False
    assert Path(LATEST_ENDPOINT_STATUS).exists()


def test_provider_live_rejects_local_endpoint(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_SERP_DISCOVERY_URL", "http://localhost:8000/serp-approved.json")
    get_settings.cache_clear()
    result = validate_provider_endpoint("serp_snippet")
    assert result["status"] == DEPLOY_READY_PENDING_HOST
    assert result["real_collection_performed"] is False
    assert "provider_endpoint_must_be_non_local_https" in result["blocked_reason"]


def test_provider_live_mock_https_success_prepares_partial_handoff(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_SERP_DISCOVERY_URL", "https://provider.example/serp-approved.json")
    get_settings.cache_clear()

    def fake_fetch(url, headers, timeout):
        assert url == "https://provider.example/serp-approved.json"
        assert headers["Accept"] == "application/json"
        assert timeout > 0
        return provider_package("serp_snippet")

    status = endpoint_status(fetch_json=fake_fetch)
    assert status["provider_live_status"] == PROVIDER_LIVE_READY
    assert status["realdata_expected_coverage"] == "partial_real_provider_coverage"
    assert status["real_collection_performed"] is True
    assert status["successful_provider_count"] == 1
