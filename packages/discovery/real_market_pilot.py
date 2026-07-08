from pathlib import Path
from typing import Any

from packages.discovery.search_engine import (
    article_candidate_from_cluster,
    search_player_needs,
    select_publish_article_candidates,
)
from packages.shared.schemas import DiscoveryDecision, DiscoverySearchRequest, PlayerNeedCluster
from packages.workflows.candidate_pipeline import (
    CandidateWorkflowResult,
    run_candidate_article_workflow,
    write_candidate_workflow_artifacts,
)


def _cluster_by_decision(decision: DiscoveryDecision) -> PlayerNeedCluster | None:
    result = search_player_needs(DiscoverySearchRequest(decisions=[decision], limit=20))
    return result.clusters[0] if result.clusters else None


def real_market_candidate_pilot(
    *,
    output_dir: str = "artifacts/candidate_drafts",
) -> dict[str, Any]:
    candidates = select_publish_article_candidates(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.publish_candidate], limit=20)
    )
    if not candidates:
        return {
            "status": "blocked",
            "reason": "No safe publish_candidate is available.",
            "publish_ready": False,
            "publishing_performed": False,
            "real_collection_performed": False,
            "candidate_only": True,
        }
    candidate = candidates[0]
    result: CandidateWorkflowResult = run_candidate_article_workflow(candidate)
    json_path, md_path = write_candidate_workflow_artifacts(candidate, result, directory=output_dir)
    watchlist = _cluster_by_decision(DiscoveryDecision.watchlist_waiting_for_answer)
    high_risk = _cluster_by_decision(DiscoveryDecision.blocked_high_risk)
    return {
        "status": "completed",
        "mode": "fixture-mock-real-market-equivalent",
        "selected_topic": {
            "candidate_id": candidate.candidate_id,
            "game_name": candidate.game_name,
            "need_key": candidate.need_key,
            "decision": candidate.decision.value,
            "risk_level": candidate.risk_level,
            "runnable": candidate.runnable,
        },
        "artifact_paths": {
            "json": str(Path(json_path)),
            "markdown": str(Path(md_path)),
        },
        "verification_status": result.verification_report.status.value if result.verification_report else "missing",
        "publish_action": result.publish_action,
        "publish_ready": False,
        "publishing_performed": False,
        "real_collection_performed": result.real_collection_performed,
        "candidate_only": True,
        "safety_fields": result.safety_fields,
        "blocked_examples": {
            "watchlist": _blocked_example(watchlist),
            "high_risk": _blocked_example(high_risk),
        },
    }


def _blocked_example(cluster: PlayerNeedCluster | None) -> dict[str, Any] | None:
    if cluster is None:
        return None
    candidate = article_candidate_from_cluster(cluster)
    return {
        "game_name": candidate.game_name,
        "need_key": candidate.need_key,
        "decision": candidate.decision.value,
        "risk_level": candidate.risk_level,
        "runnable": candidate.runnable,
        "publish_ready": candidate.publish_ready,
        "blocked_from_normal_draft": not candidate.runnable,
        "safety_flags": candidate.safety_flags,
    }
