import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from packages.discovery.real_endpoint_contract import (
    APPROVED_ENDPOINT_PROHIBITED_FIELDS,
    validate_approved_endpoint_payload,
)
from packages.discovery.real_market import (
    MAX_SNIPPET_CHARS,
    REAL_MARKET_ENDPOINT_ENV_VARS,
    REAL_MARKET_PROHIBITED_RETENTION,
    RealMarketConfigError,
    RealMarketSourceCategory,
)
from packages.shared.config import get_settings


ARTIFACT_DIR = Path("artifacts/provider_live")
LATEST_CONTRACT = ARTIFACT_DIR / "latest_provider_package_contract.json"
LATEST_ENDPOINT_STATUS = ARTIFACT_DIR / "latest_provider_endpoint_status.json"
LATEST_ENV_HANDOFF = ARTIFACT_DIR / "latest_realdata_env_handoff.json"
LATEST_READINESS = ARTIFACT_DIR / "latest_provider_live_readiness.json"

PROVIDER_ORDER: list[RealMarketSourceCategory] = ["serp_snippet", "reddit", "steam"]
PACKAGE_PATHS: dict[RealMarketSourceCategory, Path] = {
    "serp_snippet": ARTIFACT_DIR / "serp-approved.json",
    "reddit": ARTIFACT_DIR / "reddit-approved.json",
    "steam": ARTIFACT_DIR / "steam-approved.json",
}
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
PROVIDER_LIVE_READY = "partial_provider_endpoint_ready"
DEPLOY_READY_PENDING_HOST = "deploy_ready_pending_provider_host"
FAILED_CONTRACT = "failed_contract_validation"
BLOCKED_FOR_ENDPOINT = "blocked_for_provider_endpoint"
FetchJson = Callable[[str, dict[str, str], float], dict[str, Any]]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _settings_url(provider: RealMarketSourceCategory) -> str | None:
    settings = get_settings()
    return {
        "steam": settings.steam_discovery_url,
        "reddit": settings.reddit_discovery_url,
        "serp_snippet": settings.serp_discovery_url,
        "jp_community": settings.jp_community_discovery_url,
        "kr_community": settings.kr_community_discovery_url,
    }[provider]


def _endpoint_block_reason(url: str | None) -> str | None:
    if not url:
        return "missing_provider_endpoint_url"
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return "provider_endpoint_must_be_non_local_https"
    host = (parsed.hostname or "").lower()
    if host in LOCAL_HOSTS:
        return "local_provider_endpoint_not_allowed"
    if host.endswith(".local") or "fixture" in url.lower() or "mock" in url.lower():
        return "fixture_or_mock_provider_endpoint_not_allowed"
    return None


def _default_fetch_json(url: str, headers: dict[str, str], timeout: float) -> dict[str, Any]:
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(256_001)
    except URLError as exc:
        raise RealMarketConfigError(f"Provider endpoint request failed: {exc}") from exc
    if len(body) > 256_000:
        raise RealMarketConfigError("Provider endpoint payload exceeds 256000 bytes.")
    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RealMarketConfigError("Provider endpoint did not return JSON.") from exc
    if not isinstance(payload, dict):
        raise RealMarketConfigError("Provider endpoint JSON root must be an object.")
    return payload


def provider_package_contract() -> dict[str, Any]:
    artifact = {
        "artifact_type": "provider_live_package_contract",
        "generated_at": _now(),
        "providers": [
            {
                "provider_id": provider,
                "endpoint_env_var": REAL_MARKET_ENDPOINT_ENV_VARS[provider],
                "package_path": str(PACKAGE_PATHS[provider]),
                "root_fields": ["games", "questions", "source", "generated_at", "metadata"],
                "aliases_accepted_by_realdata": {"games": "hot_games", "questions": "player_questions"},
                "candidate_only": True,
                "raw_text_included": False,
                "broad_internet_coverage": False,
                "enabled_by_default": False,
            }
            for provider in PROVIDER_ORDER
        ],
        "retention_policy": {
            "max_snippet_chars": MAX_SNIPPET_CHARS,
            "prohibited_fields": sorted(set(REAL_MARKET_PROHIBITED_RETENTION) | APPROVED_ENDPOINT_PROHIBITED_FIELDS),
            "raw_full_source_allowed": False,
            "credentials_allowed": False,
        },
        "default_network_disabled": True,
        "crawler_allowed": False,
        "html_scrape_allowed": False,
        "publishing_performed": False,
    }
    _write_json(LATEST_CONTRACT, artifact)
    return artifact


def _source(provider: RealMarketSourceCategory) -> dict[str, Any]:
    return {
        "source_id": f"{provider}_approved_package_v1",
        "source_type": "approved_json_provider_package",
        "source_category": provider,
        "endpoint_type": "json",
    }


def _game(provider: RealMarketSourceCategory) -> dict[str, Any]:
    names = {
        "serp_snippet": ("provider-serp-hades-ii", "Hades II"),
        "reddit": ("provider-reddit-stardew", "Stardew Valley"),
        "steam": ("provider-steam-palworld", "Palworld"),
    }
    game_id, game_name = names[provider]
    return {
        "game_id": game_id,
        "game_name": game_name,
        "source_category": provider,
        "source_url": f"https://provider.example/{provider}/games/{game_id}",
        "rank": 1,
        "velocity": 62 if provider == "serp_snippet" else 48,
        "region": "global",
        "language": "en",
        "update_recency_days": 14,
    }


def _questions(provider: RealMarketSourceCategory) -> list[dict[str, Any]]:
    game = _game(provider)
    provider_label = {"serp_snippet": "SERP", "reddit": "Reddit", "steam": "Steam"}[provider]
    common = {
        "game_id": game["game_id"],
        "game_name": game["game_name"],
        "source_category": provider,
        "source_url": f"https://provider.example/{provider}/questions/1",
        "source_title": f"{provider_label} approved summary: common player issue",
        "language": "en",
        "region": "global",
        "engagement_count": 77,
        "reply_count": 12,
        "growth_24h": 8,
        "answer_maturity": "answered",
        "conflict_count": 0,
        "risk_level": "low",
        "snippet": "Short approved summary only. No page body, selftext, or full comments are retained.",
        "tags": ["troubleshooting", "guide-candidate"],
    }
    return [
        {
            **common,
            "question_id": f"{provider}_q_save_or_crash",
            "question_text": "Where should players look first when this issue appears?",
        },
        {
            **common,
            "question_id": f"{provider}_q_watchlist",
            "question_text": "Is there a reliable fix for this new hot issue?",
            "answer_maturity": "unanswered",
            "risk_level": "medium",
            "engagement_count": 44,
            "reply_count": 3,
        },
    ]


def provider_package(provider: RealMarketSourceCategory) -> dict[str, Any]:
    if provider not in PROVIDER_ORDER:
        raise ValueError(f"Unsupported provider package: {provider}")
    payload = {
        "games": [_game(provider)],
        "questions": _questions(provider),
        "source": _source(provider),
        "generated_at": _now(),
        "metadata": {
            "candidate_only": True,
            "provider_live_package": True,
            "raw_text_included": False,
            "raw_response_body_saved": False,
            "selftext_saved": False,
            "full_comments_saved": False,
            "broad_internet_coverage": False,
            "publish_ready": False,
            "publishing_performed": False,
        },
    }
    validate_approved_endpoint_payload(payload)
    _write_json(PACKAGE_PATHS[provider], payload)
    return payload


def write_all_packages() -> dict[str, Any]:
    return {
        "contract": provider_package_contract(),
        "packages": {provider: provider_package(provider) for provider in PROVIDER_ORDER},
    }


def validate_provider_endpoint(provider: RealMarketSourceCategory, fetch_json: FetchJson | None = None) -> dict[str, Any]:
    settings = get_settings()
    url = _settings_url(provider)
    block_reason = _endpoint_block_reason(url)
    opt_in_ready = settings.enable_discovery_real_source and settings.live_discovery_test
    base = {
        "provider_id": provider,
        "endpoint_env_var": REAL_MARKET_ENDPOINT_ENV_VARS[provider],
        "endpoint_configured": bool(url),
        "endpoint_url_stored": False,
        "endpoint_scheme": urlparse(url or "").scheme or None,
        "endpoint_host": urlparse(url or "").hostname,
        "double_opt_in_configured": opt_in_ready,
        "raw_response_body_saved": False,
        "publishing_performed": False,
        "candidate_only": True,
    }
    if block_reason or not opt_in_ready:
        return {
            **base,
            "status": DEPLOY_READY_PENDING_HOST,
            "blocked_reason": block_reason or "missing_double_opt_in",
            "real_collection_performed": False,
        }
    try:
        payload = (fetch_json or _default_fetch_json)(
            str(url),
            {"Accept": "application/json", "User-Agent": settings.connector_user_agent},
            float(settings.connector_timeout_seconds),
        )
        validation = validate_approved_endpoint_payload(payload)
        if validation["source_category"] != provider:
            raise RealMarketConfigError(
                f"Provider endpoint source_category {validation['source_category']} does not match {provider}."
            )
    except RealMarketConfigError as exc:
        return {
            **base,
            "status": FAILED_CONTRACT,
            "blocked_reason": str(exc),
            "real_collection_performed": False,
        }
    return {
        **base,
        "status": "success",
        "blocked_reason": None,
        "game_count": validation["game_count"],
        "question_count": validation["question_count"],
        "real_collection_performed": True,
    }


def endpoint_status(fetch_json: FetchJson | None = None) -> dict[str, Any]:
    results = [validate_provider_endpoint(provider, fetch_json=fetch_json) for provider in PROVIDER_ORDER]
    success = [item for item in results if item["status"] == "success"]
    artifact = {
        "artifact_type": "provider_live_endpoint_status",
        "generated_at": _now(),
        "provider_results": results,
        "successful_provider_count": len(success),
        "provider_live_status": PROVIDER_LIVE_READY if success else DEPLOY_READY_PENDING_HOST,
        "realdata_expected_coverage": "partial_real_provider_coverage" if success else "blocked_for_provider_endpoints",
        "real_collection_performed": bool(success),
        "broad_internet_coverage": False,
        "raw_response_body_saved": False,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(LATEST_ENDPOINT_STATUS, artifact)
    return artifact


def realdata_env_handoff(status: dict[str, Any] | None = None) -> dict[str, Any]:
    status = status or endpoint_status()
    commands = [
        '$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE="true"',
        '$env:PIKO_LIVE_DISCOVERY_TEST="true"',
    ]
    pending = []
    for row in status["provider_results"]:
        env_var = row["endpoint_env_var"]
        if row["status"] == "success":
            commands.append(f'$env:{env_var}="<approved {row["provider_id"]} endpoint already configured>"')
        else:
            pending.append(env_var)
            commands.append(f'# pending: set {env_var}=<non-local HTTPS approved JSON provider endpoint>')
    artifact = {
        "artifact_type": "provider_live_realdata_env_handoff",
        "generated_at": _now(),
        "provider_live_status": status["provider_live_status"],
        "realdata_expected_coverage": status["realdata_expected_coverage"],
        "powershell_commands": commands,
        "successful_providers": [row["provider_id"] for row in status["provider_results"] if row["status"] == "success"],
        "pending_provider_env_vars": pending,
        "contains_secrets": False,
        "candidate_only": True,
    }
    _write_json(LATEST_ENV_HANDOFF, artifact)
    return artifact


def readiness(status: dict[str, Any] | None = None, handoff: dict[str, Any] | None = None) -> dict[str, Any]:
    status = status or endpoint_status()
    handoff = handoff or realdata_env_handoff(status)
    artifact = {
        "artifact_type": "provider_live_readiness",
        "generated_at": _now(),
        "provider_live_status": status["provider_live_status"],
        "realdata_expected_coverage": status["realdata_expected_coverage"],
        "successful_provider_count": status["successful_provider_count"],
        "pending_provider_env_vars": handoff["pending_provider_env_vars"],
        "partial_provider_endpoint_ready": status["successful_provider_count"] > 0,
        "real_collection_performed": status["real_collection_performed"],
        "broad_internet_coverage": False,
        "publish_ready": False,
        "publishing_performed": False,
        "upload_performed": False,
        "deployment_performed": False,
        "crawler_used": False,
        "html_scrape_used": False,
        "raw_response_body_saved": False,
        "full_posts_saved": False,
        "full_pages_saved": False,
        "full_comments_saved": False,
        "credentials_stored": False,
        "secrets_retained": False,
        "llm_called": False,
    }
    _write_json(LATEST_READINESS, artifact)
    return artifact


def build_provider_live_artifacts(fetch_json: FetchJson | None = None) -> dict[str, Any]:
    packages = write_all_packages()
    status = endpoint_status(fetch_json=fetch_json)
    handoff = realdata_env_handoff(status)
    ready = readiness(status, handoff)
    return {
        "contract": packages["contract"],
        "packages": packages["packages"],
        "endpoint_status": status,
        "env_handoff": handoff,
        "readiness": ready,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build provider-live approved JSON packages.")
    parser.add_argument("--write-artifacts", action="store_true")
    args = parser.parse_args()
    result = build_provider_live_artifacts() if args.write_artifacts else readiness()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

