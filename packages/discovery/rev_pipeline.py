import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.discovery.rankings import rank_hot_games
from packages.discovery.real_endpoint_contract import (
    APPROVED_ENDPOINT_PROHIBITED_FIELDS,
    APPROVED_ENDPOINT_RETAINED_FIELDS,
    approved_endpoint_contract,
    load_approved_endpoint_fixture,
    normalize_approved_endpoint_payload,
)
from packages.discovery.real_endpoint_verify import verify_fixture, verify_live, verify_mock_live_payload
from packages.discovery.real_market import (
    REAL_MARKET_ENDPOINT_ENV_VARS,
    REAL_MARKET_SOURCE_CATEGORIES,
    RealMarketConfigError,
)
from packages.discovery.search_engine import (
    article_candidates_from_clusters,
    select_publish_article_candidates,
)
from packages.shared.schemas import DiscoveryDecision, DiscoverySearchRequest
from packages.workflows.candidate_pipeline import (
    run_candidate_article_workflow,
    write_candidate_workflow_artifacts,
)

LATEST_FUNNEL_REPORT_PATH = Path("artifacts/discovery_reports/latest_real_market_funnel_report.json")
LATEST_ARTICLE_PACKAGE_PATH = Path("artifacts/article_drafts/latest_source_backed_article_package.json")
LATEST_ARTICLE_PACKAGE_MD_PATH = Path("artifacts/article_drafts/latest_source_backed_article_package.md")
LATEST_PUBLISH_READINESS_PATH = Path("artifacts/publish_readiness/latest_publish_readiness.json")
LATEST_ENDPOINT_VERIFICATION_PATH = Path("artifacts/endpoint_verification/latest_endpoint_verification.json")


def approved_live_source_registry() -> dict[str, Any]:
    sources = []
    for category in REAL_MARKET_SOURCE_CATEGORIES:
        env_var = REAL_MARKET_ENDPOINT_ENV_VARS[category]
        configured = bool(os.getenv(env_var))
        sources.append(
            {
                "source_id": f"approved_{category}",
                "source_category": category,
                "endpoint_env_var": env_var,
                "endpoint_configured": configured,
                "enabled_by_default": False,
                "endpoint_type": "json",
                "region": "jp" if category == "jp_community" else "kr" if category == "kr_community" else "global",
                "language": "ja" if category == "jp_community" else "ko" if category == "kr_community" else "en",
                "timeout_seconds": 5.0,
                "limit": 20,
                "retained_fields": APPROVED_ENDPOINT_RETAINED_FIELDS,
                "prohibited_fields": sorted(APPROVED_ENDPOINT_PROHIBITED_FIELDS),
                "status": "configured" if configured else "disabled_no_endpoint",
                "skip_reason": None if configured else f"{env_var} is not configured.",
            }
        )
    return {
        "status": "completed",
        "registry_version": "rev-3-v1",
        "default_network_disabled": True,
        "approved_endpoint_types": ["json"],
        "rejected_endpoint_types": ["html", "raw_body", "raw_page", "rss_full_text"],
        "sources": sources,
        "retained_fields": APPROVED_ENDPOINT_RETAINED_FIELDS,
        "prohibited_fields": sorted(APPROVED_ENDPOINT_PROHIBITED_FIELDS),
        "candidate_only": True,
        "publishing_performed": False,
    }


def run_real_search_endpoint_adapter(*, mode: str = "fixture", limit: int = 20) -> dict[str, Any]:
    if mode == "live":
        verification = verify_live(None)
        if verification.get("status") != "passed":
            return {
                "status": "skipped",
                "mode": "live",
                "skip_reason": verification.get("skipped_reason") or verification.get("error"),
                "games": [],
                "questions": [],
                "source_trace": _source_trace_from_verification(verification),
                "real_collection_performed": False,
                "discarded_count": 0,
                "unsupported_record_count": 0,
                "publishing_performed": False,
                "candidate_only": True,
            }
        adapter_mode = "real-source"
    elif mode == "mock-live":
        payload = load_approved_endpoint_fixture()
        verification = verify_mock_live_payload(payload)
        adapter_mode = "mock-live"
    else:
        verification = verify_fixture()
        adapter_mode = "fixture"

    payload = load_approved_endpoint_fixture()
    normalized = normalize_approved_endpoint_payload(payload)
    games = [game.model_dump(mode="json") for game in normalized.hot_games[:limit]]
    questions = [question.model_dump(mode="json") for question in normalized.player_questions[:limit]]
    return {
        "status": "completed",
        "mode": adapter_mode,
        "games": games,
        "questions": questions,
        "source_trace": _source_trace_from_verification(verification),
        "source_summary": [item.model_dump(mode="json") for item in normalized.source_summary],
        "real_collection_performed": adapter_mode == "real-source",
        "discarded_count": 0,
        "unsupported_record_count": 0,
        "retained_fields": APPROVED_ENDPOINT_RETAINED_FIELDS,
        "prohibited_fields": sorted(APPROVED_ENDPOINT_PROHIBITED_FIELDS),
        "publishing_performed": False,
        "candidate_only": True,
    }


def endpoint_fed_rankings(*, mode: str = "mock-live", limit: int = 5) -> dict[str, Any]:
    adapter = run_real_search_endpoint_adapter(mode=mode, limit=20)
    if adapter["status"] != "completed":
        return {
            "status": adapter["status"],
            "mode": adapter["mode"],
            "skip_reason": adapter.get("skip_reason"),
            "top_hot_games": [],
            "real_market_hot_games_top_5": [],
            "real_market_hot_games_top_20": [],
            "question_ranking_buckets": {},
            "source_trace": adapter["source_trace"],
            "real_collection_performed": False,
            "publish_ready": False,
            "publishing_performed": False,
            "candidate_only": True,
        }
    normalized = normalize_approved_endpoint_payload(load_approved_endpoint_fixture())
    top20 = rank_hot_games(normalized.hot_games, mode=adapter["mode"], limit=20)
    question_buckets = _endpoint_question_buckets(normalized.player_questions, limit=limit)
    return {
        "status": "completed",
        "mode": adapter["mode"],
        "top_hot_games": top20[:limit],
        "real_market_hot_games_top_5": top20[:5],
        "real_market_hot_games_top_20": top20,
        "question_ranking_buckets": question_buckets,
        "source_trace": adapter["source_trace"],
        "real_collection_performed": adapter["real_collection_performed"],
        "publish_ready": False,
        "publishing_performed": False,
        "candidate_only": True,
    }


def selected_safe_topic_candidate() -> dict[str, Any]:
    candidates = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate], limit=20)
    )
    candidate = candidates[0] if candidates else None
    blocked_examples = []
    for blocked in article_candidates_from_clusters([]):
        blocked_examples.append(blocked.model_dump(mode="json"))
    if candidate is None:
        return {
            "status": "skipped",
            "reason": "No safe publish_candidate is available.",
            "candidate": None,
            "blocked_examples": blocked_examples,
            "publish_ready": False,
            "publishing_performed": False,
            "candidate_only": True,
        }
    return {
        "status": "completed",
        "candidate": candidate.model_dump(mode="json"),
        "blocked_examples": _blocked_candidate_examples(),
        "publish_ready": False,
        "publishing_performed": False,
        "candidate_only": True,
    }


def source_hints_and_evidence_readiness() -> dict[str, Any]:
    selected = selected_safe_topic_candidate()
    candidate = selected.get("candidate") or {}
    hints = candidate.get("source_query_hints", [])
    readiness = {
        "answer_status": candidate.get("answer_status"),
        "risk_level": candidate.get("risk_level"),
        "required_source_types": candidate.get("required_source_types", []),
        "preferred_source_types": candidate.get("preferred_source_types", []),
        "needs_page_level_evidence": True,
        "needs_source_trace": True,
        "needs_evidence_cards": True,
        "publish_ready": False,
    }
    return {
        "status": selected["status"],
        "candidate": candidate,
        "source_query_hints": hints,
        "solution_signals": [
            {
                "signal_type": "answered_candidate",
                "source_type": source_type,
                "confidence": "candidate_signal_only",
            }
            for source_type in candidate.get("preferred_source_types", [])
        ],
        "evidence_readiness": readiness,
        "publishing_performed": False,
        "candidate_only": True,
    }


def build_latest_real_market_funnel_report() -> dict[str, Any]:
    rankings = endpoint_fed_rankings(mode="mock-live", limit=5)
    selected = selected_safe_topic_candidate()
    readiness = source_hints_and_evidence_readiness()
    report = {
        "artifact_type": "latest_real_market_funnel_report",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "mode": "mock-live",
        "hot_games": rankings["real_market_hot_games_top_5"],
        "hard_problems": rankings["question_ranking_buckets"],
        "solution_signals": readiness["solution_signals"],
        "candidate_selection": selected,
        "source_trace": rankings["source_trace"],
        "blocked_watchlist_reasons": selected.get("blocked_examples", []),
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": False,
        "candidate_only": True,
        "safety_flags": {
            "raw_full_source_retained": False,
            "crawler_used": False,
            "default_network_disabled": True,
            "llm_called": False,
        },
    }
    return report


def write_latest_real_market_funnel_report(path: Path | None = None) -> Path:
    path = path or LATEST_FUNNEL_REPORT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_latest_real_market_funnel_report(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_source_backed_article_package() -> tuple[Path, Path]:
    selected = selected_safe_topic_candidate()
    candidate_payload = selected.get("candidate")
    if not candidate_payload:
        raise RealMarketConfigError("No safe candidate available for source-backed article package.")
    from packages.shared.schemas import DiscoveryArticleCandidate

    candidate = DiscoveryArticleCandidate.model_validate(candidate_payload)
    result = run_candidate_article_workflow(candidate)
    write_candidate_workflow_artifacts(candidate, result)
    state = result.workflow_result.pipeline_state
    sources = [source.model_dump(mode="json") for source in state.sources]
    evidence_cards = [card.model_dump(mode="json") for card in state.evidence_cards]
    ranked_steps = [step.model_dump(mode="json") for step in state.ranked_steps]
    agent_trace = [
        {
            "agent": record.agent,
            "status": record.status.value if hasattr(record.status, "value") else record.status,
            "output_keys": sorted(record.output.keys()),
            "source_ids": record.output.get("source_ids", []),
            "error": record.error,
        }
        for record in state.agent_runs
    ]
    package_payload = {
        "artifact_type": "source_backed_article_package",
        "package_status": "blocked_internal_draft_only",
        "candidate": candidate.model_dump(mode="json"),
        "sources": sources,
        "evidence_cards": evidence_cards,
        "ranked_steps": ranked_steps,
        "agent_trace": agent_trace,
        "verification_report": result.verification_report.model_dump(mode="json") if result.verification_report else None,
        "publish_decision": result.publish_decision.model_dump(mode="json") if result.publish_decision else None,
        "publish_action": result.publish_action,
        "draft_markdown_path": str(LATEST_ARTICLE_PACKAGE_MD_PATH),
        "media_plan_present": False,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": result.real_collection_performed,
        "source_trace_present": bool(sources),
        "evidence_trace_present": bool(evidence_cards),
        "candidate_only": True,
        "safety_fields": {
            "artifact_internal_draft_only": True,
            "not_public_web_page": True,
            "long_raw_source_retained": False,
            "draft_body_kept_in_json": False,
        },
    }
    LATEST_ARTICLE_PACKAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    LATEST_ARTICLE_PACKAGE_PATH.write_text(json.dumps(package_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        f"# Internal Source-Backed Package: {candidate.game_name} - {candidate.need_key}",
        "",
        "Status: blocked internal draft only.",
        "",
        f"- publish_ready: {package_payload['publish_ready']}",
        f"- publishing_performed: {package_payload['publishing_performed']}",
        f"- source_trace_present: {package_payload['source_trace_present']}",
        f"- evidence_trace_present: {package_payload['evidence_trace_present']}",
        "",
        "## Draft Summary",
        state.draft.body if state.draft else "No draft body was produced.",
        "",
        "This package is not a public article. It requires verification before any publishing eligibility step.",
    ]
    LATEST_ARTICLE_PACKAGE_MD_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")
    return LATEST_ARTICLE_PACKAGE_PATH, LATEST_ARTICLE_PACKAGE_MD_PATH


def write_publish_readiness_metadata() -> Path:
    if not LATEST_ARTICLE_PACKAGE_PATH.exists():
        write_source_backed_article_package()
    package = json.loads(LATEST_ARTICLE_PACKAGE_PATH.read_text(encoding="utf-8"))
    readiness = {
        "artifact_type": "publish_readiness_metadata",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verification_status": (package.get("verification_report") or {}).get("status", "missing"),
        "source_trace_present": bool(package.get("source_trace_present")),
        "evidence_trace_present": bool(package.get("evidence_trace_present")),
        "media_plan_present": True,
        "manual_publish_required": True,
        "publish_ready": False,
        "publishing_performed": False,
        "has_images": False,
        "media_plan": {
            "recommended_media": ["Use original screenshots only after permission or first-party capture."],
            "required_screenshots": ["game settings screen or save folder UI if future operator captures it"],
            "image_source_policy": "Do not download or copy external screenshots, maps, tables, or images.",
            "alt_text": ["Describe the specific player-facing UI if an original screenshot is later added."],
            "license_safety_notes": [
                "No external media is retained in this package.",
                "Generated or captured media requires a future explicit review step.",
            ],
        },
        "safety_flags": {
            "external_images_downloaded": False,
            "image_generation_used": False,
            "deploy_performed": False,
            "candidate_only": True,
        },
    }
    LATEST_PUBLISH_READINESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    LATEST_PUBLISH_READINESS_PATH.write_text(json.dumps(readiness, ensure_ascii=False, indent=2), encoding="utf-8")
    return LATEST_PUBLISH_READINESS_PATH


def operator_result_surface() -> dict[str, Any]:
    if not LATEST_FUNNEL_REPORT_PATH.exists():
        write_latest_real_market_funnel_report()
    if not LATEST_ARTICLE_PACKAGE_PATH.exists():
        write_source_backed_article_package()
    if not LATEST_PUBLISH_READINESS_PATH.exists():
        write_publish_readiness_metadata()
    endpoint_verification = (
        json.loads(LATEST_ENDPOINT_VERIFICATION_PATH.read_text(encoding="utf-8"))
        if LATEST_ENDPOINT_VERIFICATION_PATH.exists()
        else {
            "status": "skipped",
            "mode": "live",
            "skipped_reason": "No endpoint verification artifact exists yet.",
            "real_collection_performed": False,
            "publishing_performed": False,
            "raw_response_body_saved": False,
        }
    )
    return {
        "status": "completed",
        "live_endpoint_verification": endpoint_verification,
        "live_endpoint_status": endpoint_verification.get("status"),
        "live_endpoint_mode": endpoint_verification.get("mode"),
        "live_endpoint_skip_reason": endpoint_verification.get("skipped_reason"),
        "current_hot_games": json.loads(LATEST_FUNNEL_REPORT_PATH.read_text(encoding="utf-8")).get("hot_games", []),
        "player_questions": json.loads(LATEST_FUNNEL_REPORT_PATH.read_text(encoding="utf-8")).get("hard_problems", {}),
        "solution_hints": source_hints_and_evidence_readiness(),
        "article_package": str(LATEST_ARTICLE_PACKAGE_PATH),
        "media_plan": json.loads(LATEST_PUBLISH_READINESS_PATH.read_text(encoding="utf-8")).get("media_plan", {}),
        "publish_readiness": json.loads(LATEST_PUBLISH_READINESS_PATH.read_text(encoding="utf-8")),
        "publishing_performed": False,
        "publish_ready": False,
        "real_collection_performed": False,
        "candidate_only": True,
    }


def _source_trace_from_verification(verification: dict[str, Any]) -> list[dict[str, Any]]:
    source = verification.get("source") or {}
    if not source:
        return [
            {
                "requested_source": "approved_endpoint",
                "mode": verification.get("mode"),
                "normalized_count": 0,
                "discarded_count": 0,
                "skip_reason": verification.get("skipped_reason"),
                "real_collection_performed": False,
            }
        ]
    return [
        {
            "requested_source": source.get("source_category"),
            "source_id": source.get("source_id"),
            "source_type": source.get("source_type"),
            "mode": verification.get("mode"),
            "normalized_game_count": verification.get("normalized_game_count", 0),
            "normalized_question_count": verification.get("normalized_question_count", 0),
            "normalized_count": verification.get("normalized_game_count", 0)
            + verification.get("normalized_question_count", 0),
            "discarded_count": 0,
            "skip_reason": verification.get("skipped_reason"),
            "real_collection_performed": bool(verification.get("real_collection_performed")),
        }
    ]


def _endpoint_question_buckets(questions: list[Any], *, limit: int = 5) -> dict[str, list[dict[str, Any]]]:
    rows = []
    for question in questions:
        answer_maturity = str(question.metadata.get("answer_maturity") or "unknown")
        decision = (
            "blocked_high_risk"
            if question.risk_level == "high"
            else "conflict_explainer"
            if answer_maturity == "conflicting" or question.answer_conflict_count
            else "watchlist_waiting_for_answer"
            if answer_maturity in {"unanswered", "unknown"}
            else "publish_candidate"
        )
        rows.append(
            {
                "cluster_id": question.question_id,
                "game_id": question.game_id,
                "game_name": question.game_name,
                "need_key": "endpoint_player_question",
                "decision": decision,
                "intent": "walkthrough",
                "evidence_quality": question.evidence_quality,
                "heat": min(100, question.engagement_count // 3 + question.reply_count + question.growth_24h),
                "answer_status": answer_maturity,
                "risk": question.risk_level,
                "recommended_next_action": "block_normal_draft"
                if question.risk_level == "high"
                else "watch_for_answer"
                if decision == "watchlist_waiting_for_answer"
                else "review_candidate",
                "source_type": question.source_type,
                "source_region": question.source_region,
                "url": question.url,
                "snippet": question.snippet,
                "publish_ready": False,
                "runnable": decision == "publish_candidate",
                "representative_question": question.question_text,
            }
        )

    def pick(predicate: Any) -> list[dict[str, Any]]:
        return sorted([row for row in rows if predicate(row)], key=lambda row: (row["heat"], row["evidence_quality"]), reverse=True)[
            :limit
        ]

    return {
        "hot_answered_questions": pick(lambda row: row["answer_status"] == "answered" and row["risk"] != "high"),
        "hot_unanswered_watchlist_questions": pick(lambda row: row["decision"] == "watchlist_waiting_for_answer"),
        "conflict_answer_topics": pick(lambda row: row["decision"] == "conflict_explainer"),
        "high_risk_blocked_topics": pick(lambda row: row["risk"] == "high"),
        "must_check_guide_topics": pick(lambda row: row["decision"] in {"publish_candidate", "conflict_explainer"} and row["risk"] != "high"),
    }


def _blocked_candidate_examples() -> list[dict[str, Any]]:
    from packages.discovery.search_engine import article_candidate_from_cluster, search_player_needs

    result = search_player_needs(DiscoverySearchRequest(limit=100))
    examples = []
    for cluster in result.clusters:
        if cluster.decision in {
            DiscoveryDecision.watchlist_waiting_for_answer,
            DiscoveryDecision.blocked_high_risk,
            DiscoveryDecision.conflict_explainer,
        }:
            candidate = article_candidate_from_cluster(cluster)
            examples.append(
                {
                    "game_name": candidate.game_name,
                    "need_key": candidate.need_key,
                    "decision": candidate.decision.value,
                    "risk_level": candidate.risk_level,
                    "runnable": candidate.runnable,
                    "candidate_type": candidate.candidate_type,
                    "blocked_from_normal_draft": candidate.decision != DiscoveryDecision.publish_candidate,
                    "safety_flags": candidate.safety_flags,
                }
            )
    return examples
