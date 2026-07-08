import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from packages.discovery.real_endpoint_contract import (
    approved_endpoint_contract,
    validate_approved_endpoint_payload,
)
from packages.discovery.real_endpoint_verify import verify_live, write_endpoint_verification_artifact
from packages.discovery.real_market import RealMarketConfigError
from packages.shared.config import get_settings


ARTIFACT_DIR = Path("artifacts/external_endpoint")
EXTERNAL_SCOPE = "external_approved_endpoint"
BLOCKED = "blocked_for_external_endpoint"
FAILED_CONTRACT = "failed_contract_validation"
SUCCESS = "success"
REQUIRED_ENV = ["PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "PIKO_LIVE_DISCOVERY_TEST", "PIKO_APPROVED_ENDPOINT_URL"]
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _endpoint_summary(url: str | None) -> dict[str, Any]:
    if not url:
        return {"endpoint_url_present": False, "endpoint_scheme": None, "endpoint_host": None, "endpoint_url_stored": False}
    parsed = urlparse(url)
    return {
        "endpoint_url_present": True,
        "endpoint_scheme": parsed.scheme,
        "endpoint_host": parsed.hostname,
        "endpoint_url_stored": False,
    }


def _external_endpoint_block_reason(url: str | None) -> str | None:
    if not url:
        return "missing_external_endpoint_url"
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "endpoint_must_be_http_json"
    if (parsed.hostname or "").lower() in LOCAL_HOSTS:
        return "localhost_not_allowed_for_external_endpoint"
    if parsed.scheme in {"file", "fixture"}:
        return "local_fixture_url_not_allowed_for_external_endpoint"
    return None


def external_endpoint_approval_contract() -> dict[str, Any]:
    artifact = {
        "artifact_type": "external_endpoint_approval_contract",
        "generated_at": _now(),
        "endpoint_required": True,
        "endpoint_type": "json",
        "operator_approved_required": True,
        "allowed_scope": EXTERNAL_SCOPE,
        "broad_internet_coverage": False,
        "rejected_endpoint_types": ["html", "rss", "raw_body", "crawler", "file", "fixture", "localhost"],
        "max_payload_bytes": 256_000,
        "timeout_seconds": get_settings().connector_timeout_seconds,
        "publish_ready": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "external_endpoint_approval.json", artifact)
    return artifact


def external_endpoint_readiness() -> dict[str, Any]:
    settings = get_settings()
    endpoint = os.getenv("PIKO_APPROVED_ENDPOINT_URL")
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    block_reason = _external_endpoint_block_reason(endpoint)
    ready = settings.enable_discovery_real_source and settings.live_discovery_test and endpoint and block_reason is None
    artifact = {
        "artifact_type": "external_endpoint_readiness",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "ready" if ready else BLOCKED,
        "required_env": REQUIRED_ENV,
        "missing_config": missing,
        "blocked_reason": None if ready else block_reason or "missing_required_opt_in",
        **_endpoint_summary(endpoint),
        "double_opt_in_configured": settings.enable_discovery_real_source and settings.live_discovery_test,
        "broad_internet_coverage": False,
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "external_endpoint_readiness.json", artifact)
    return artifact


def external_http_probe() -> dict[str, Any]:
    readiness = external_endpoint_readiness()
    if readiness["status"] != "ready":
        artifact = {
            "artifact_type": "external_http_probe",
            "generated_at": _now(),
            "scope": EXTERNAL_SCOPE,
            "status": BLOCKED,
            "blocked_reason": readiness["blocked_reason"],
            "missing_config": readiness["missing_config"],
            "timeout_seconds": get_settings().connector_timeout_seconds,
            "max_payload_bytes": 256_000,
            "real_collection_performed": False,
            "raw_response_body_saved": False,
            "publishing_performed": False,
            "broad_internet_coverage": False,
            "candidate_only": True,
        }
        write_endpoint_verification_artifact(artifact)
        _write_json(ARTIFACT_DIR / "external_http_probe.json", artifact)
        return artifact

    try:
        verification = verify_live(None)
    except RealMarketConfigError as exc:
        artifact = {
            "artifact_type": "external_http_probe",
            "generated_at": _now(),
            "scope": EXTERNAL_SCOPE,
            "status": FAILED_CONTRACT,
            "error": str(exc),
            "real_collection_performed": False,
            "raw_response_body_saved": False,
            "publishing_performed": False,
            "broad_internet_coverage": False,
            "candidate_only": True,
        }
        write_endpoint_verification_artifact(artifact)
        _write_json(ARTIFACT_DIR / "external_http_probe.json", artifact)
        return artifact

    success = verification.get("status") == "passed" and verification.get("real_collection_performed") is True
    artifact = {
        "artifact_type": "external_http_probe",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": SUCCESS if success else FAILED_CONTRACT,
        "source": verification.get("source"),
        "normalized_game_count": verification.get("normalized_game_count", 0),
        "normalized_question_count": verification.get("normalized_question_count", 0),
        "ranking_count": verification.get("ranking_count", 0),
        "ranking_preview": verification.get("ranking_preview", {}),
        "retained_fields": verification.get("retained_fields", []),
        "real_collection_performed": bool(success),
        "raw_response_body_saved": False,
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    write_endpoint_verification_artifact(artifact)
    _write_json(ARTIFACT_DIR / "external_http_probe.json", artifact)
    return artifact


def validate_external_payload_contract(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        validation = validate_approved_endpoint_payload(payload)
    except RealMarketConfigError as exc:
        return {
            "artifact_type": "external_contract_validation",
            "generated_at": _now(),
            "scope": EXTERNAL_SCOPE,
            "status": FAILED_CONTRACT,
            "error": str(exc),
            "real_collection_performed": False,
            "publishing_performed": False,
        }
    return {
        "artifact_type": "external_contract_validation",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "valid",
        "game_count": validation["game_count"],
        "question_count": validation["question_count"],
        "retained_fields": validation["retained_fields"],
        "prohibited_fields": validation["prohibited_fields"],
        "real_collection_performed": False,
        "publishing_performed": False,
    }


def external_contract_validation_artifact() -> dict[str, Any]:
    probe = external_http_probe()
    status = "valid" if probe["status"] == SUCCESS else probe["status"]
    artifact = {
        "artifact_type": "external_contract_validation",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": status,
        "blocked_reason": probe.get("blocked_reason"),
        "normalized_game_count": probe.get("normalized_game_count", 0),
        "normalized_question_count": probe.get("normalized_question_count", 0),
        "contract": approved_endpoint_contract(),
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "publishing_performed": False,
        "broad_internet_coverage": False,
    }
    _write_json(ARTIFACT_DIR / "external_contract_validation.json", artifact)
    return artifact


def external_collection_safety_summary() -> dict[str, Any]:
    probe = external_http_probe()
    artifact = {
        "artifact_type": "external_collection_safety_summary",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": probe["status"],
        "raw_response_body_saved": False,
        "full_posts_saved": False,
        "full_pages_saved": False,
        "full_comments_saved": False,
        "secrets_retained": False,
        "crawler_used": False,
        "html_scrape_used": False,
        "broad_internet_coverage": False,
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "external_collection_safety_summary.json", artifact)
    return artifact


def external_normalized_signals() -> dict[str, Any]:
    probe = external_http_probe()
    preview = probe.get("ranking_preview", {}) if probe["status"] == SUCCESS else {}
    signals = [
        {
            "signal_type": "hot_game",
            "source_id": (probe.get("source") or {}).get("source_id"),
            "source_type": (probe.get("source") or {}).get("source_type"),
            "scope": EXTERNAL_SCOPE,
            "candidate": candidate,
        }
        for candidate in preview.get("top_hot_games", [])[:5]
    ]
    artifact = {
        "artifact_type": "external_normalized_signals",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": probe["status"],
        "signals": signals,
        "signal_count": len(signals),
        "need_clusters": [],
        "blocked_reason": probe.get("blocked_reason"),
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "external_normalized_signals.json", artifact)
    return artifact


def external_connector_feedback() -> dict[str, Any]:
    probe = external_http_probe()
    artifact = {
        "artifact_type": "external_connector_feedback",
        "generated_at": _now(),
        "connector_id": "approved_json_endpoint",
        "scope": EXTERNAL_SCOPE,
        "last_external_probe_status": probe["status"],
        "readiness_delta": "external_probe_success" if probe["status"] == SUCCESS else "blocked_or_failed_no_activation",
        "live_ready_candidate": probe["status"] == SUCCESS,
        "production_activation_allowed": False,
        "next_action": "piko_verify_external_endpoint" if probe["status"] == SUCCESS else "configure_external_endpoint_and_re_run",
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "publishing_performed": False,
        "broad_internet_coverage": False,
    }
    _write_json(ARTIFACT_DIR / "external_connector_feedback.json", artifact)
    return artifact


def real_external_handoff() -> dict[str, Any]:
    probe = external_http_probe()
    preview = probe.get("ranking_preview", {}) if probe["status"] == SUCCESS else {}
    artifact = {
        "artifact_type": "real_external_handoff",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "completed" if probe["status"] == SUCCESS else probe["status"],
        "top_candidates": preview.get("top_hot_games", [])[:5],
        "pain_buckets": preview.get("question_buckets", {}),
        "source_trace": [
            {
                "scope": EXTERNAL_SCOPE,
                "status": probe["status"],
                "source_id": (probe.get("source") or {}).get("source_id"),
                "real_collection_performed": bool(probe.get("real_collection_performed")),
            }
        ],
        "blocked_reason": probe.get("blocked_reason"),
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "real_external_handoff.json", artifact)
    _write_json(Path("artifacts/real_data_pilot/latest_external_endpoint_handoff.json"), artifact)
    return artifact


def external_candidate_article_package() -> dict[str, Any]:
    handoff = real_external_handoff()
    answered = (handoff.get("pain_buckets") or {}).get("hot_answered_questions", [])
    candidate = answered[0] if answered else None
    artifact = {
        "artifact_type": "external_candidate_article_package",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": "ready_for_internal_evidence_pipeline" if candidate else handoff["status"],
        "selected_topic": candidate,
        "source_trace": handoff.get("source_trace", []),
        "evidence_trace": []
        if candidate is None
        else [
            {
                "source_id": (handoff.get("source_trace") or [{}])[0].get("source_id"),
                "question_id": candidate.get("question_id"),
                "trace_type": "external_approved_endpoint_signal",
            }
        ],
        "outline": [
            "Player need",
            "External approved endpoint signal",
            "Evidence still required before draft",
            "Risk and source trace",
        ],
        "no_candidate_reason": None if candidate else handoff.get("blocked_reason") or handoff["status"],
        "verification_required": True,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": bool(handoff.get("real_collection_performed")),
        "broad_internet_coverage": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "external_candidate_article_package.json", artifact)
    _write_json(Path("artifacts/article_drafts/latest_external_endpoint_candidate_package.json"), artifact)
    return artifact


def operator_external_endpoint_result() -> dict[str, Any]:
    readiness = external_endpoint_readiness()
    probe = external_http_probe()
    handoff = real_external_handoff()
    package = external_candidate_article_package()
    artifact = {
        "artifact_type": "operator_external_endpoint_result",
        "generated_at": _now(),
        "scope": EXTERNAL_SCOPE,
        "status": probe["status"],
        "readiness_status": readiness["status"],
        "blocked_reason": probe.get("blocked_reason") or readiness.get("blocked_reason"),
        "normalized_counts": {
            "games": probe.get("normalized_game_count", 0),
            "questions": probe.get("normalized_question_count", 0),
        },
        "handoff_status": handoff["status"],
        "candidate_status": package["status"],
        "real_collection_performed": bool(probe.get("real_collection_performed")),
        "publish_ready": False,
        "publishing_performed": False,
        "broad_internet_coverage": False,
        "read_only_surface": True,
    }
    _write_json(ARTIFACT_DIR / "operator_external_endpoint_result.json", artifact)
    return artifact


def operator_external_endpoint_html() -> str:
    result = operator_external_endpoint_result()
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko External Endpoint</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "dl{display:grid;grid-template-columns:230px minmax(0,1fr);gap:8px;max-width:900px}"
        "dt{font-weight:700}dd{margin:0}.blocked{color:#9f1239}.ok{color:#166534}</style></head>"
        "<body><h1>External Approved Endpoint Result</h1>"
        "<p>Approved JSON endpoint only. This is not broad internet coverage.</p><dl>"
        f"<dt>Scope</dt><dd>{result['scope']}</dd>"
        f"<dt>Status</dt><dd class='blocked'>{result['status']}</dd>"
        f"<dt>Real collection performed</dt><dd>{str(result['real_collection_performed']).lower()}</dd>"
        f"<dt>Broad internet coverage</dt><dd>{str(result['broad_internet_coverage']).lower()}</dd>"
        f"<dt>Blocked reason</dt><dd>{result.get('blocked_reason') or ''}</dd>"
        f"<dt>Candidate status</dt><dd>{result['candidate_status']}</dd>"
        "</dl><p>No crawler, HTML scrape, non-approved broad connector, publishing, deploy, or LLM path is active.</p></body></html>"
    )


def build_external_endpoint_artifacts() -> dict[str, Any]:
    return {
        "approval": external_endpoint_approval_contract(),
        "readiness": external_endpoint_readiness(),
        "probe": external_http_probe(),
        "contract_validation": external_contract_validation_artifact(),
        "safety": external_collection_safety_summary(),
        "signals": external_normalized_signals(),
        "feedback": external_connector_feedback(),
        "handoff": real_external_handoff(),
        "candidate_package": external_candidate_article_package(),
        "operator_result": operator_external_endpoint_result(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the external approved endpoint pilot.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write all external endpoint pilot artifacts.")
    args = parser.parse_args()
    result = build_external_endpoint_artifacts() if args.write_artifacts else operator_external_endpoint_result()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
