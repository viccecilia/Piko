import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from packages.discovery.rankings import rank_hot_games
from packages.discovery.real_endpoint_contract import (
    APPROVED_ENDPOINT_FIXTURE_PATH,
    approved_endpoint_contract,
    approved_endpoint_safety_flags,
    load_approved_endpoint_fixture,
    normalize_approved_endpoint_payload,
    validate_approved_endpoint_payload,
)
from packages.discovery.real_market import RealMarketConfigError
from packages.shared.config import get_settings

MAX_APPROVED_ENDPOINT_BYTES = 256_000
DEFAULT_ENDPOINT_ARTIFACT_DIR = Path("artifacts/endpoint_verification")


def _fetch_json_endpoint(url: str) -> dict[str, Any]:
    settings = get_settings()
    request = Request(url, headers={"Accept": "application/json", "User-Agent": settings.connector_user_agent})
    try:
        with urlopen(request, timeout=settings.connector_timeout_seconds) as response:
            payload_bytes = response.read(MAX_APPROVED_ENDPOINT_BYTES + 1)
    except URLError as exc:
        raise RealMarketConfigError(f"Approved endpoint request failed: {exc}") from exc
    if len(payload_bytes) > MAX_APPROVED_ENDPOINT_BYTES:
        raise RealMarketConfigError("Approved endpoint response exceeds the bounded verification payload size.")
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RealMarketConfigError("Approved endpoint did not return JSON.") from exc
    if not isinstance(payload, dict):
        raise RealMarketConfigError("Approved endpoint JSON root must be an object.")
    return payload


def _question_buckets(normalized_questions: list[Any]) -> dict[str, list[dict[str, Any]]]:
    buckets: dict[str, list[dict[str, Any]]] = {
        "hot_answered_questions": [],
        "hot_unanswered_watchlist_questions": [],
        "conflict_answer_topics": [],
        "high_risk_blocked_topics": [],
    }

    def row(question: Any) -> dict[str, Any]:
        answer_maturity = str(question.metadata.get("answer_maturity") or "unknown")
        heat = min(100, question.engagement_count // 3 + question.reply_count + question.growth_24h)
        return {
            "question_id": question.question_id,
            "game_name": question.game_name,
            "question_text": question.question_text,
            "source_type": question.source_type,
            "source_region": question.source_region,
            "answer_maturity": answer_maturity,
            "risk_level": question.risk_level,
            "heat": heat,
            "evidence_quality": question.evidence_quality,
            "recommended_next_action": "block_normal_draft"
            if question.risk_level == "high"
            else "watch_for_answer"
            if answer_maturity in {"unanswered", "unknown"}
            else "review_candidate",
            "publish_ready": False,
            "runnable": question.risk_level != "high" and answer_maturity == "answered",
        }

    for question in normalized_questions:
        item = row(question)
        answer_maturity = item["answer_maturity"]
        if item["risk_level"] == "high":
            item["runnable"] = False
            buckets["high_risk_blocked_topics"].append(item)
        elif answer_maturity == "answered":
            buckets["hot_answered_questions"].append(item)
        elif answer_maturity in {"unanswered", "unknown"}:
            item["runnable"] = False
            buckets["hot_unanswered_watchlist_questions"].append(item)
        if answer_maturity == "conflicting" or question.answer_conflict_count > 0:
            item["runnable"] = False
            buckets["conflict_answer_topics"].append(item)

    return {
        key: sorted(value, key=lambda row: (row["heat"], row["evidence_quality"]), reverse=True)[:5]
        for key, value in buckets.items()
    }


def verify_endpoint_payload(payload: dict[str, Any], *, mode: str) -> dict[str, Any]:
    validation = validate_approved_endpoint_payload(payload)
    normalized = normalize_approved_endpoint_payload(payload)
    hot_game_rankings = rank_hot_games(normalized.hot_games, mode=mode, limit=5)
    source = payload["source"]
    real_collection_performed = mode == "real-source"
    return {
        "status": "passed",
        "mode": mode,
        "source_count": 1,
        "source": {
            "source_id": source.get("source_id"),
            "source_type": source.get("source_type"),
            "source_category": source.get("source_category"),
            "endpoint_type": source.get("endpoint_type"),
        },
        "generated_at": payload.get("generated_at"),
        "normalized_game_count": len(normalized.hot_games),
        "normalized_question_count": len(normalized.player_questions),
        "ranking_count": len(hot_game_rankings),
        "ranking_preview": {
            "top_hot_games": hot_game_rankings,
            "question_buckets": _question_buckets(normalized.player_questions),
        },
        "retained_fields": validation["retained_fields"],
        "prohibited_fields": validation["prohibited_fields"],
        "skipped_reason": None,
        "safety_flags": approved_endpoint_safety_flags(),
        "real_collection_performed": real_collection_performed,
        "publishing_performed": False,
        "candidate_only": True,
        "raw_response_body_saved": False,
    }


def verify_fixture() -> dict[str, Any]:
    payload = load_approved_endpoint_fixture(APPROVED_ENDPOINT_FIXTURE_PATH)
    result = verify_endpoint_payload(payload, mode="fixture")
    result["fixture_path"] = str(APPROVED_ENDPOINT_FIXTURE_PATH)
    result["real_collection_performed"] = False
    return result


def verify_live(url: str | None) -> dict[str, Any]:
    settings = get_settings()
    if not (settings.enable_discovery_real_source and settings.live_discovery_test):
        return {
            "status": "skipped",
            "mode": "live",
            "source_count": 0,
            "normalized_game_count": 0,
            "normalized_question_count": 0,
            "retained_fields": approved_endpoint_contract()["retained_fields"],
            "skipped_reason": (
                "Live endpoint verification requires PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true "
                "and PIKO_LIVE_DISCOVERY_TEST=true."
            ),
            "safety_flags": approved_endpoint_safety_flags(),
            "real_collection_performed": False,
            "publishing_performed": False,
            "candidate_only": True,
            "raw_response_body_saved": False,
        }
    endpoint = url or os.getenv("PIKO_APPROVED_ENDPOINT_URL")
    if not endpoint:
        return {
            "status": "skipped",
            "mode": "live",
            "source_count": 0,
            "normalized_game_count": 0,
            "normalized_question_count": 0,
            "retained_fields": approved_endpoint_contract()["retained_fields"],
            "skipped_reason": "Live endpoint verification requires --url or PIKO_APPROVED_ENDPOINT_URL.",
            "safety_flags": approved_endpoint_safety_flags(),
            "real_collection_performed": False,
            "publishing_performed": False,
            "candidate_only": True,
            "raw_response_body_saved": False,
        }
    payload = _fetch_json_endpoint(endpoint)
    result = verify_endpoint_payload(payload, mode="real-source")
    result["endpoint_url"] = endpoint
    return result


def verify_mock_live_payload(payload: dict[str, Any]) -> dict[str, Any]:
    result = verify_endpoint_payload(payload, mode="mock-live")
    result["real_collection_performed"] = False
    return result


def write_endpoint_verification_artifact(
    result: dict[str, Any],
    *,
    directory: str | Path = DEFAULT_ENDPOINT_ARTIFACT_DIR,
    filename: str = "latest_endpoint_verification.json",
) -> Path:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    artifact = {
        "artifact_type": "endpoint_verification_summary",
        "status": result.get("status"),
        "mode": result.get("mode"),
        "source": result.get("source"),
        "endpoint_category": (result.get("source") or {}).get("source_category"),
        "normalized_game_count": result.get("normalized_game_count", 0),
        "normalized_question_count": result.get("normalized_question_count", 0),
        "ranking_count": result.get("ranking_count", 0),
        "retained_fields": result.get("retained_fields", []),
        "skipped_reason": result.get("skipped_reason"),
        "safety_flags": result.get("safety_flags", {}),
        "real_collection_performed": result.get("real_collection_performed", False),
        "publishing_performed": False,
        "raw_response_body_saved": False,
        "candidate_only": True,
    }
    path = target / filename
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify approved Piko real-market JSON endpoint payloads.")
    parser.add_argument("--fixture", action="store_true", help="Verify the local approved endpoint fixture mirror.")
    parser.add_argument("--live", action="store_true", help="Verify a live approved JSON endpoint with explicit opt-in.")
    parser.add_argument("--url", default=None, help="Approved live endpoint URL. Requires --live and opt-in env vars.")
    parser.add_argument("--write-artifact", action="store_true", help="Write a bounded verification summary artifact.")
    args = parser.parse_args()
    try:
        if args.live:
            result = verify_live(args.url)
        else:
            result = verify_fixture()
    except RealMarketConfigError as exc:
        result = {
            "status": "failed",
            "mode": "live" if args.live else "fixture",
            "error": str(exc),
            "safety_flags": approved_endpoint_safety_flags(),
            "real_collection_performed": False,
            "publishing_performed": False,
            "candidate_only": True,
        }
    if args.write_artifact:
        result["artifact_path"] = str(write_endpoint_verification_artifact(result))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
