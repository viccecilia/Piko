import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.connector_registry.pipeline import RETAINED_FIELDS, PROHIBITED_SOURCE_FIELDS, sanitize_payload
from packages.discovery.real_endpoint_verify import verify_live, write_endpoint_verification_artifact
from packages.discovery.real_market import RealMarketConfigError


ARTIFACT_DIR = Path("artifacts/live_connector_pilot")
REAL_HANDOFF_DIR = Path("artifacts/real_data_pilot")
DISCOVERY_REPORT_DIR = Path("artifacts/discovery_reports")
SELECTED_CONNECTOR_ID = "approved_json_endpoint"
BLOCKED_FOR_ENDPOINT = "blocked_for_endpoint"
FAILED_CONTRACT_VALIDATION = "failed_contract_validation"
SUCCESS = "success"
REQUIRED_ENV = [
    "PIKO_ENABLE_DISCOVERY_REAL_SOURCE",
    "PIKO_LIVE_DISCOVERY_TEST",
    "PIKO_APPROVED_ENDPOINT_URL",
]
FORBIDDEN_LIVE_CONNECTORS = ["steam", "reddit", "jp_community", "kr_community", "serp", "mediawiki"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return path


def _env_ready() -> tuple[bool, list[str]]:
    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    return not missing, missing


def live_connector_selection() -> dict[str, Any]:
    payload = {
        "artifact_type": "live_connector_selection",
        "generated_at": _now(),
        "selected_connector_id": SELECTED_CONNECTOR_ID,
        "selected_source_type": "approved_json_endpoint",
        "selection_reason": "Lowest-risk connector: bounded JSON endpoint with existing contract validation.",
        "excluded_connectors": [
            {"connector": connector, "live_enabled": False, "reason": "outside_live_connector_v1_scope"}
            for connector in FORBIDDEN_LIVE_CONNECTORS
        ],
        "only_approved_json_endpoint_allowed": True,
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "live_connector_selection.json", payload)
    return payload


def live_connector_approval() -> dict[str, Any]:
    payload = {
        "artifact_type": "live_connector_approval",
        "generated_at": _now(),
        "connector_id": SELECTED_CONNECTOR_ID,
        "live_probe_allowed": True,
        "collection_allowed": "only_when_double_opt_in_and_endpoint_present",
        "allowed_endpoint_type": "json",
        "max_payload_bytes": 256_000,
        "timeout_seconds": 5,
        "max_records": 20,
        "production_activation_allowed": False,
        "forbidden_connectors": FORBIDDEN_LIVE_CONNECTORS,
        "raw_response_body_saved": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "live_connector_approval.json", payload)
    return payload


def endpoint_readiness() -> dict[str, Any]:
    ready, missing = _env_ready()
    payload = {
        "artifact_type": "live_connector_endpoint_readiness",
        "generated_at": _now(),
        "connector_id": SELECTED_CONNECTOR_ID,
        "status": "ready" if ready else BLOCKED_FOR_ENDPOINT,
        "required_env": REQUIRED_ENV,
        "missing_config": missing,
        "endpoint_configured": "PIKO_APPROVED_ENDPOINT_URL" not in missing,
        "double_opt_in_configured": "PIKO_ENABLE_DISCOVERY_REAL_SOURCE" not in missing
        and "PIKO_LIVE_DISCOVERY_TEST" not in missing,
        "endpoint_url_stored": False,
        "real_collection_performed": False,
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "endpoint_readiness.json", payload)
    return payload


def bounded_endpoint_verification() -> dict[str, Any]:
    readiness = endpoint_readiness()
    if readiness["status"] != "ready":
        result = {
            "artifact_type": "bounded_endpoint_verification",
            "generated_at": _now(),
            "status": BLOCKED_FOR_ENDPOINT,
            "connector_id": SELECTED_CONNECTOR_ID,
            "mode": "live",
            "missing_config": readiness["missing_config"],
            "blocked_reason": BLOCKED_FOR_ENDPOINT,
            "real_collection_performed": False,
            "publishing_performed": False,
            "raw_response_body_saved": False,
            "candidate_only": True,
        }
        write_endpoint_verification_artifact(result)
        _write_json(ARTIFACT_DIR / "bounded_endpoint_verification.json", result)
        return result

    try:
        verification = verify_live(None)
    except RealMarketConfigError as exc:
        result = {
            "artifact_type": "bounded_endpoint_verification",
            "generated_at": _now(),
            "status": FAILED_CONTRACT_VALIDATION,
            "connector_id": SELECTED_CONNECTOR_ID,
            "mode": "live",
            "error": str(exc),
            "real_collection_performed": False,
            "publishing_performed": False,
            "raw_response_body_saved": False,
            "candidate_only": True,
        }
        write_endpoint_verification_artifact(result)
        _write_json(ARTIFACT_DIR / "bounded_endpoint_verification.json", result)
        return result

    status = SUCCESS if verification.get("status") == "passed" and verification.get("real_collection_performed") else FAILED_CONTRACT_VALIDATION
    result = {
        "artifact_type": "bounded_endpoint_verification",
        "generated_at": _now(),
        "status": status,
        "connector_id": SELECTED_CONNECTOR_ID,
        "mode": verification.get("mode"),
        "source": verification.get("source"),
        "normalized_game_count": verification.get("normalized_game_count", 0),
        "normalized_question_count": verification.get("normalized_question_count", 0),
        "ranking_count": verification.get("ranking_count", 0),
        "ranking_preview": verification.get("ranking_preview", {}),
        "retained_fields": verification.get("retained_fields", []),
        "safety_flags": verification.get("safety_flags", {}),
        "real_collection_performed": status == SUCCESS,
        "publishing_performed": False,
        "raw_response_body_saved": False,
        "candidate_only": True,
        "failed_reason": None if status == SUCCESS else verification.get("skipped_reason") or verification.get("error") or "verification_not_passed",
    }
    write_endpoint_verification_artifact(result)
    _write_json(ARTIFACT_DIR / "bounded_endpoint_verification.json", result)
    return result


def bounded_live_collection_artifact() -> dict[str, Any]:
    verification = bounded_endpoint_verification()
    payload = {
        "artifact_type": "bounded_live_collection_artifact",
        "generated_at": _now(),
        "status": verification["status"],
        "connector_id": SELECTED_CONNECTOR_ID,
        "real_collection_performed": bool(verification.get("real_collection_performed")),
        "normalized_counts": {
            "games": verification.get("normalized_game_count", 0),
            "questions": verification.get("normalized_question_count", 0),
        },
        "payload_size_bounds": {"max_payload_bytes": 256_000, "max_records": 20},
        "blocked_reason": verification.get("blocked_reason") or verification.get("failed_reason"),
        "raw_body_saved": False,
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "bounded_live_collection.json", payload)
    return payload


def normalized_live_signals() -> dict[str, Any]:
    verification = bounded_endpoint_verification()
    if verification["status"] != SUCCESS:
        signals: list[dict[str, Any]] = []
    else:
        preview = verification.get("ranking_preview", {})
        signals = [
            sanitize_payload(
                {
                    "signal_type": "hot_game",
                    "source_id": (verification.get("source") or {}).get("source_id"),
                    "source_type": (verification.get("source") or {}).get("source_type"),
                    "candidate": item,
                }
            )
            for item in preview.get("top_hot_games", [])[:5]
        ]
    payload = {
        "artifact_type": "normalized_live_connector_signals",
        "generated_at": _now(),
        "status": verification["status"],
        "connector_id": SELECTED_CONNECTOR_ID,
        "signals": signals,
        "signal_count": len(signals),
        "retained_fields": RETAINED_FIELDS,
        "prohibited_fields": PROHIBITED_SOURCE_FIELDS,
        "blocked_reason": verification.get("blocked_reason") or verification.get("failed_reason"),
        "real_collection_performed": bool(verification.get("real_collection_performed")),
        "publishing_performed": False,
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "normalized_live_signals.json", payload)
    return payload


def connector_registry_feedback() -> dict[str, Any]:
    verification = bounded_endpoint_verification()
    status = verification["status"]
    payload = {
        "artifact_type": "live_connector_registry_feedback",
        "generated_at": _now(),
        "connector_id": SELECTED_CONNECTOR_ID,
        "last_probe_status": status,
        "last_probe_at": _now(),
        "readiness_delta": "live_probe_success" if status == SUCCESS else "blocked_or_failed_no_activation",
        "production_activation_allowed": False,
        "live_ready": status == SUCCESS,
        "next_action": "operator_verify_live_payload" if status == SUCCESS else "configure_approved_endpoint_and_re_run",
        "real_collection_performed": bool(verification.get("real_collection_performed")),
        "publishing_performed": False,
    }
    _write_json(ARTIFACT_DIR / "connector_registry_feedback.json", payload)
    return payload


def real_funnel_handoff() -> dict[str, Any]:
    signals = normalized_live_signals()
    status = signals["status"]
    payload = {
        "artifact_type": "live_connector_real_funnel_handoff",
        "generated_at": _now(),
        "status": "handoff_ready" if status == SUCCESS and signals["signal_count"] else status,
        "connector_id": SELECTED_CONNECTOR_ID,
        "hot_game_candidates": signals["signals"] if status == SUCCESS else [],
        "need_clusters": [],
        "source_trace": [
            {
                "connector_id": SELECTED_CONNECTOR_ID,
                "status": status,
                "signal_count": signals["signal_count"],
                "real_collection_performed": signals["real_collection_performed"],
            }
        ],
        "blocked_reason": signals.get("blocked_reason"),
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": bool(signals.get("real_collection_performed")),
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "real_funnel_handoff.json", payload)
    _write_json(REAL_HANDOFF_DIR / "latest_live_connector_handoff.json", payload)
    return payload


def candidate_only_ranking_preview() -> dict[str, Any]:
    handoff = real_funnel_handoff()
    candidates = handoff["hot_game_candidates"][:5] if handoff["status"] == "handoff_ready" else []
    payload = {
        "artifact_type": "live_connector_candidate_only_ranking_preview",
        "generated_at": _now(),
        "status": "completed" if candidates else handoff["status"],
        "connector_id": SELECTED_CONNECTOR_ID,
        "top_candidates": candidates,
        "blocked_reason": handoff.get("blocked_reason"),
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": bool(handoff.get("real_collection_performed")),
        "candidate_only": True,
    }
    _write_json(ARTIFACT_DIR / "candidate_only_ranking_preview.json", payload)
    _write_json(DISCOVERY_REPORT_DIR / "latest_live_connector_ranking_preview.json", payload)
    return payload


def operator_live_connector_surface() -> dict[str, Any]:
    selection = live_connector_selection()
    approval = live_connector_approval()
    readiness = endpoint_readiness()
    verification = bounded_endpoint_verification()
    collection = bounded_live_collection_artifact()
    signals = normalized_live_signals()
    handoff = real_funnel_handoff()
    preview = candidate_only_ranking_preview()
    payload = {
        "artifact_type": "operator_live_connector_surface",
        "generated_at": _now(),
        "connector_id": SELECTED_CONNECTOR_ID,
        "selection": selection,
        "approval": approval,
        "endpoint_readiness": readiness,
        "probe_status": verification["status"],
        "collection_status": collection["status"],
        "normalized_counts": collection["normalized_counts"],
        "handoff_status": handoff["status"],
        "ranking_preview_status": preview["status"],
        "blocked_reason": verification.get("blocked_reason") or verification.get("failed_reason"),
        "real_collection_performed": bool(verification.get("real_collection_performed")),
        "publish_ready": False,
        "publishing_performed": False,
        "candidate_only": True,
        "read_only_surface": True,
    }
    _write_json(ARTIFACT_DIR / "operator_live_connector_surface.json", payload)
    return payload


def operator_live_connector_window_html() -> str:
    surface = operator_live_connector_surface()
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Piko Live Connector</title>"
        "<style>body{font-family:Arial,sans-serif;margin:24px;color:#172033}"
        "dl{display:grid;grid-template-columns:220px minmax(0,1fr);gap:8px;max-width:900px}"
        "dt{font-weight:700}dd{margin:0}.blocked{color:#9f1239}.ok{color:#166534}</style></head>"
        "<body><h1>Live Connector Pilot</h1><p>Read-only. Only approved_json_endpoint is eligible.</p>"
        "<dl>"
        f"<dt>Connector</dt><dd>{surface['connector_id']}</dd>"
        f"<dt>Probe status</dt><dd class='blocked'>{surface['probe_status']}</dd>"
        f"<dt>Real collection performed</dt><dd>{str(surface['real_collection_performed']).lower()}</dd>"
        f"<dt>Blocked reason</dt><dd>{surface.get('blocked_reason') or ''}</dd>"
        f"<dt>Handoff status</dt><dd>{surface['handoff_status']}</dd>"
        f"<dt>Ranking preview</dt><dd>{surface['ranking_preview_status']}</dd>"
        "</dl><p>No Steam, Reddit, JP, KR, SERP, crawler, publishing, deploy, or LLM path is active.</p>"
        "</body></html>"
    )


def build_live_connector_artifacts() -> dict[str, Any]:
    return {
        "selection": live_connector_selection(),
        "approval": live_connector_approval(),
        "readiness": endpoint_readiness(),
        "verification": bounded_endpoint_verification(),
        "collection": bounded_live_collection_artifact(),
        "signals": normalized_live_signals(),
        "feedback": connector_registry_feedback(),
        "handoff": real_funnel_handoff(),
        "ranking_preview": candidate_only_ranking_preview(),
        "operator_surface": operator_live_connector_surface(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the bounded approved_json_endpoint live connector pilot.")
    parser.add_argument("--write-artifacts", action="store_true", help="Write all live connector pilot artifacts.")
    args = parser.parse_args()
    result = build_live_connector_artifacts() if args.write_artifacts else operator_live_connector_surface()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
