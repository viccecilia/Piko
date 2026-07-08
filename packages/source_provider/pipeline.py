import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen

from packages.discovery.real_endpoint_contract import (
    APPROVED_ENDPOINT_FIXTURE_PATH,
    approved_endpoint_contract,
    load_approved_endpoint_fixture,
    validate_approved_endpoint_payload,
)
from packages.discovery.real_market import RealMarketConfigError
from packages.shared.config import get_settings


ARTIFACT_DIR = Path("artifacts/source_provider")
PACKAGE_DIR = ARTIFACT_DIR / "static_endpoint_package"
PAYLOAD_PATH = PACKAGE_DIR / "approved-market.json"
README_PATH = PACKAGE_DIR / "README.md"
STATUS_DEPLOY_READY = "deploy_ready_pending_host"
STATUS_BLOCKED_URL = "blocked_for_external_url"
STATUS_VALIDATED = "validated_external_url"
STATUS_FAILED_CONTRACT = "failed_contract_validation"
PROVIDER_SCOPE = "deploy_ready_static_json"
EXTERNAL_SCOPE = "external_approved_endpoint"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}
MAX_PROVIDER_FETCH_BYTES = 256_000


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate_url() -> str | None:
    return os.getenv("PIKO_EXTERNAL_APPROVED_ENDPOINT_URL") or os.getenv("PIKO_APPROVED_ENDPOINT_URL")


def _is_external_url(url: str | None) -> tuple[bool, str | None]:
    if not url:
        return False, "missing_external_url"
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False, "url_must_be_http_or_https"
    host = (parsed.hostname or "").lower()
    if host in LOCAL_HOSTS:
        return False, "localhost_not_external"
    if parsed.scheme in {"file", "fixture"}:
        return False, "local_fixture_not_external"
    return True, None


def _redacted_url(url: str | None) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    safe = parsed._replace(query="[REDACTED]" if parsed.query else "", fragment="")
    return urlunparse(safe)


def provider_strategy_artifact() -> dict[str, Any]:
    providers = [
        {"provider": "GitHub Raw / Gist raw URL", "recommended_for_first_try": True, "requires_credentials_in_piko": False},
        {"provider": "Cloudflare Pages static JSON", "recommended_for_first_try": True, "requires_credentials_in_piko": False},
        {"provider": "Vercel / Netlify static JSON", "recommended_for_first_try": True, "requires_credentials_in_piko": False},
        {"provider": "User-owned HTTPS API endpoint", "recommended_for_first_try": False, "requires_credentials_in_piko": False},
    ]
    artifact = {
        "artifact_type": "source_provider_strategy",
        "generated_at": _now(),
        "recommended_strategy": "static_json_provider_package_first",
        "providers": providers,
        "invalid_external_providers": ["localhost", "127.0.0.1", "file", "fixture", "raw_html_page"],
        "deployment_performed": False,
        "credentials_stored": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "provider_strategy.json", artifact)
    return artifact


def provider_approval_contract() -> dict[str, Any]:
    artifact = {
        "artifact_type": "source_provider_approval_contract",
        "generated_at": _now(),
        "provider_type": "static_json_or_operator_owned_https_json",
        "external_url_required": True,
        "operator_approval_required": True,
        "credential_storage_allowed": False,
        "deployment_allowed": False,
        "prohibited_providers": ["localhost", "127.0.0.1", "file", "fixture", "raw_html_page", "crawler"],
        "approved_endpoint_contract": approved_endpoint_contract(),
        "external_provider_validated": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "provider_approval_contract.json", artifact)
    return artifact


def provider_payload() -> dict[str, Any]:
    payload = load_approved_endpoint_fixture(APPROVED_ENDPOINT_FIXTURE_PATH)
    payload.setdefault("metadata", {})
    payload["metadata"] = {
        **payload["metadata"],
        "provider_package_scope": PROVIDER_SCOPE,
        "deploy_ready": True,
        "external_provider_validated": False,
        "broad_internet_coverage": False,
        "raw_text_included": False,
        "candidate_only": True,
    }
    validate_approved_endpoint_payload(payload)
    return payload


def approved_payload_package_artifact() -> dict[str, Any]:
    payload = provider_payload()
    _write_json(PAYLOAD_PATH, payload)
    validation = validate_approved_endpoint_payload(payload)
    artifact = {
        "artifact_type": "approved_json_payload_package",
        "generated_at": _now(),
        "provider_package_scope": PROVIDER_SCOPE,
        "payload_path": str(PAYLOAD_PATH),
        "contract_valid": validation["status"] == "valid",
        "game_count": validation["game_count"],
        "question_count": validation["question_count"],
        "prohibited_fields_present": False,
        "external_provider_validated": False,
        "deployment_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "approved_payload_package.json", artifact)
    return artifact


def static_endpoint_package_artifact() -> dict[str, Any]:
    approved_payload_package_artifact()
    readme = """# Piko Approved JSON Endpoint Package

This package contains a static JSON payload that conforms to Piko's approved endpoint contract.

Files:

- `approved-market.json`

Suggested hosting options:

- GitHub Raw or Gist raw URL
- Cloudflare Pages static asset
- Vercel or Netlify static asset
- User-owned HTTPS JSON endpoint

Rules:

- Do not host it as HTML.
- Do not add raw source bodies, full posts, full comments, credentials, tokens, cookies, API keys, or authorization headers.
- Do not treat localhost, file, or fixture URLs as external endpoints.
- After hosting, set the resulting non-local HTTPS URL in `PIKO_APPROVED_ENDPOINT_URL` and rerun EXTERNAL-ENDPOINT.
"""
    _write_text(README_PATH, readme)
    artifact = {
        "artifact_type": "static_endpoint_package",
        "generated_at": _now(),
        "package_dir": str(PACKAGE_DIR),
        "payload_path": str(PAYLOAD_PATH),
        "readme_path": str(README_PATH),
        "contract_valid": validate_approved_endpoint_payload(json.loads(PAYLOAD_PATH.read_text(encoding="utf-8")))["status"] == "valid",
        "upload_performed": False,
        "deployment_performed": False,
        "credentials_stored": False,
    }
    _write_json(ARTIFACT_DIR / "static_endpoint_package.json", artifact)
    return artifact


def package_manifest_artifact() -> dict[str, Any]:
    static_endpoint_package_artifact()
    artifact = {
        "artifact_type": "source_provider_package_manifest",
        "generated_at": _now(),
        "package_version": "source-provider-v1",
        "payload_path": str(PAYLOAD_PATH),
        "payload_hash_sha256": _hash_file(PAYLOAD_PATH),
        "contract_version": "approved_endpoint_v1",
        "safety_flags": {
            "raw_body_saved": False,
            "secrets_retained": False,
            "credentials_stored": False,
            "upload_performed": False,
            "deployment_performed": False,
            "broad_internet_coverage": False,
        },
    }
    _write_json(ARTIFACT_DIR / "package_manifest.json", artifact)
    return artifact


def _fetch_external_payload(url: str) -> dict[str, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": get_settings().connector_user_agent})
    try:
        with urlopen(request, timeout=get_settings().connector_timeout_seconds) as response:
            payload_bytes = response.read(MAX_PROVIDER_FETCH_BYTES + 1)
    except URLError as exc:
        raise RealMarketConfigError(f"External provider request failed: {exc}") from exc
    if len(payload_bytes) > MAX_PROVIDER_FETCH_BYTES:
        raise RealMarketConfigError("External provider response exceeds payload size limit.")
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RealMarketConfigError("External provider did not return JSON.") from exc
    if not isinstance(payload, dict):
        raise RealMarketConfigError("External provider JSON root must be an object.")
    return payload


def external_url_validation_artifact() -> dict[str, Any]:
    url = _candidate_url()
    is_external, reason = _is_external_url(url)
    if not url:
        status = STATUS_DEPLOY_READY
    elif not is_external:
        status = STATUS_BLOCKED_URL
    else:
        try:
            payload = _fetch_external_payload(url)
            validation = validate_approved_endpoint_payload(payload)
            status = STATUS_VALIDATED
            reason = None
            game_count = validation["game_count"]
            question_count = validation["question_count"]
        except RealMarketConfigError as exc:
            status = STATUS_FAILED_CONTRACT
            reason = str(exc)
            game_count = 0
            question_count = 0
    artifact = {
        "artifact_type": "external_url_validation",
        "generated_at": _now(),
        "status": status,
        "external_provider_validated": status == STATUS_VALIDATED,
        "approved_url_redacted": _redacted_url(url),
        "blocked_reason": reason,
        "game_count": locals().get("game_count", 0),
        "question_count": locals().get("question_count", 0),
        "real_collection_performed": status == STATUS_VALIDATED,
        "raw_response_body_saved": False,
        "credentials_stored": False,
        "deployment_performed": False,
        "broad_internet_coverage": False,
    }
    _write_json(ARTIFACT_DIR / "external_url_validation.json", artifact)
    return artifact


def provider_status_artifact() -> dict[str, Any]:
    strategy = provider_strategy_artifact()
    package = package_manifest_artifact()
    validation = external_url_validation_artifact()
    status = validation["status"]
    artifact = {
        "artifact_type": "source_provider_status",
        "generated_at": _now(),
        "provider_status": status,
        "external_provider_validated": validation["external_provider_validated"],
        "approved_url_redacted": validation["approved_url_redacted"],
        "blocked_reason": validation["blocked_reason"],
        "package_path": package["payload_path"],
        "payload_hash_sha256": package["payload_hash_sha256"],
        "next_action": "set_external_endpoint_env_and_rerun_external_endpoint"
        if status == STATUS_VALIDATED
        else "host_static_endpoint_package_then_rerun_validation",
        "strategy": strategy["recommended_strategy"],
        "deployment_performed": False,
        "credentials_stored": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "provider_status.json", artifact)
    return artifact


def piko_env_handoff_artifact() -> dict[str, Any]:
    status = provider_status_artifact()
    ready = status["external_provider_validated"]
    url_value = status["approved_url_redacted"] if ready else "<external approved json url>"
    artifact = {
        "artifact_type": "piko_external_endpoint_env_handoff",
        "generated_at": _now(),
        "ready_to_run_external": ready,
        "provider_status": status["provider_status"],
        "instructions": [
            '$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"',
            '$env:PIKO_LIVE_DISCOVERY_TEST = "true"',
            f'$env:PIKO_APPROVED_ENDPOINT_URL = "{url_value}"',
            "python -m packages.external_endpoint.pipeline --write-artifacts",
        ],
        "placeholder_used": not ready,
        "secrets_included": False,
        "global_env_modified": False,
        "deployment_performed": False,
    }
    _write_json(ARTIFACT_DIR / "piko_env_handoff.json", artifact)
    return artifact


def operator_instructions_artifact() -> dict[str, Any]:
    static_endpoint_package_artifact()
    markdown = """# Source Provider Operator Instructions

1. Review `artifacts/source_provider/static_endpoint_package/approved-market.json`.
2. Host that JSON file on an operator-approved non-local HTTP(S) URL.
3. Do not add credentials, tokens, cookies, API keys, authorization headers, raw source bodies, full posts, or full comments.
4. Validate the hosted URL by setting:

```powershell
$env:PIKO_ENABLE_DISCOVERY_REAL_SOURCE = "true"
$env:PIKO_LIVE_DISCOVERY_TEST = "true"
$env:PIKO_APPROVED_ENDPOINT_URL = "<external approved json url>"
python -m packages.source_provider.pipeline --write-artifacts
```

5. If validated, rerun EXTERNAL-ENDPOINT with the same URL.

No upload or deployment was performed by this worker.
"""
    path = ARTIFACT_DIR / "operator_instructions.md"
    _write_text(path, markdown)
    artifact = {
        "artifact_type": "source_provider_operator_instructions",
        "generated_at": _now(),
        "markdown_path": str(path),
        "contains_secrets": False,
        "deployment_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "operator_instructions.json", artifact)
    return artifact


def operator_surface_artifact() -> dict[str, Any]:
    status = provider_status_artifact()
    artifact = {
        "artifact_type": "source_provider_operator_surface",
        "generated_at": _now(),
        "provider_status": status["provider_status"],
        "package_path": status["package_path"],
        "external_provider_validated": status["external_provider_validated"],
        "approved_url_redacted": status["approved_url_redacted"],
        "blocked_reason": status["blocked_reason"],
        "next_action": status["next_action"],
        "upload_performed": False,
        "deployment_performed": False,
        "credentials_stored": False,
        "publishing_performed": False,
        "read_only_surface": True,
    }
    _write_json(ARTIFACT_DIR / "operator_surface.json", artifact)
    return artifact


def operator_surface_html() -> str:
    surface = operator_surface_artifact()
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Source Provider</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "dl{display:grid;grid-template-columns:230px minmax(0,1fr);gap:8px;max-width:900px}"
        "dt{font-weight:700}dd{margin:0}.pending{color:#92400e}.ok{color:#166534}</style></head>"
        "<body><h1>Source Provider Package</h1>"
        "<p>Deploy-ready package only. No upload or deployment was performed.</p><dl>"
        f"<dt>Status</dt><dd class='pending'>{surface['provider_status']}</dd>"
        f"<dt>Package path</dt><dd>{surface['package_path']}</dd>"
        f"<dt>External provider validated</dt><dd>{str(surface['external_provider_validated']).lower()}</dd>"
        f"<dt>Approved URL</dt><dd>{surface.get('approved_url_redacted') or ''}</dd>"
        f"<dt>Next action</dt><dd>{surface['next_action']}</dd>"
        "</dl><p>No tokens, credentials, crawler, scraping, publishing, or remote deployment are active.</p></body></html>"
    )


def build_source_provider_artifacts() -> dict[str, Any]:
    return {
        "strategy": provider_strategy_artifact(),
        "approval": provider_approval_contract(),
        "payload": approved_payload_package_artifact(),
        "static_package": static_endpoint_package_artifact(),
        "manifest": package_manifest_artifact(),
        "url_validation": external_url_validation_artifact(),
        "status": provider_status_artifact(),
        "env_handoff": piko_env_handoff_artifact(),
        "operator_instructions": operator_instructions_artifact(),
        "operator_surface": operator_surface_artifact(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare and validate a Piko approved JSON source provider package.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write all source provider artifacts.")
    args = parser.parse_args()
    result = build_source_provider_artifacts() if args.write_artifacts else operator_surface_artifact()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
