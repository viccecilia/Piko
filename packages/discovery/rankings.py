from collections import defaultdict
from typing import Any

from packages.discovery.scoring import score_game_heat
from packages.discovery.search_engine import search_player_needs
from packages.shared.schemas import DiscoverySearchRequest, GameHeatSignal, PlayerNeedCluster


GAME_TYPE_LABELS = {
    "stardew_valley": "生活模拟 / 农场经营",
    "hades_ii": "动作 Roguelike",
    "hollow_knight": "银河城 / 探索动作",
}


AUDIENCE_PROFILES = {
    "female_interest_fit": {
        "label": "女生兴趣向",
        "description": "偏生活模拟、收集探索、低风险、可一步步解决的问题。不是对真实玩家性别做判断。",
    },
    "male_interest_fit": {
        "label": "男生兴趣向",
        "description": "偏动作挑战、性能调参、Bug 修复、Build/路线优化的问题。不是对真实玩家性别做判断。",
    },
    "handheld_players": {
        "label": "掌机/Steam Deck 玩家",
        "description": "关注帧率、设置、兼容性、存档迁移与低风险操作。",
    },
    "new_players": {
        "label": "新手玩家",
        "description": "关注路径、任务、基础 Build、避免剧透和单页清晰答案。",
    },
    "completionists": {
        "label": "收集/探索玩家",
        "description": "关注地图路线、隐藏物品、NPC/任务链和长期可用攻略。",
    },
}


def _guide_need_score(cluster: PlayerNeedCluster) -> int:
    risk_penalty = {"low": 0, "medium": 12, "high": 40}[cluster.risk_level]
    conflict_bonus = 8 if cluster.answer_status == "conflicting" else 0
    watch_bonus = 10 if cluster.decision == "watchlist_waiting_for_answer" else 0
    score = (
        round(cluster.heat_score * 0.3)
        + round(cluster.content_opportunity_score * 0.35)
        + round(cluster.actionability_score * 0.15)
        + round(cluster.evidence_quality * 0.12)
        + round(cluster.region_signal_score * 0.08)
        + conflict_bonus
        + watch_bonus
        - risk_penalty
    )
    return max(0, min(100, score))


def _audience_scores(cluster: PlayerNeedCluster) -> dict[str, int]:
    text = f"{cluster.need_key} {cluster.search_intent} {' '.join(cluster.normalization_hints)}".lower()
    base = _guide_need_score(cluster)
    scores = {
        "female_interest_fit": base,
        "male_interest_fit": base,
        "handheld_players": base,
        "new_players": base,
        "completionists": base,
    }
    if cluster.game_id == "stardew_valley" or any(term in text for term in ["save", "location", "quest"]):
        scores["female_interest_fit"] += 14
        scores["new_players"] += 10
    if cluster.game_id == "hades_ii" or any(term in text for term in ["bug", "settings", "build", "crash"]):
        scores["male_interest_fit"] += 14
        scores["handheld_players"] += 12
    if any(term in text for term in ["map", "hidden", "quest", "location"]):
        scores["completionists"] += 16
    if "steam_deck" in " ".join(cluster.source_search_hints).lower() or cluster.search_intent == "settings":
        scores["handheld_players"] += 18
    if cluster.risk_level == "high":
        scores["female_interest_fit"] -= 20
        scores["male_interest_fit"] -= 20
        scores["new_players"] -= 20
    return {key: max(0, min(100, value)) for key, value in scores.items()}


def _game_summary(clusters: list[PlayerNeedCluster]) -> list[dict[str, Any]]:
    grouped: dict[str, list[PlayerNeedCluster]] = defaultdict(list)
    for cluster in clusters:
        grouped[cluster.game_id].append(cluster)

    rows = []
    for game_id, items in grouped.items():
        top_cluster = max(items, key=_guide_need_score)
        guide_need_score = max(_guide_need_score(item) for item in items)
        publish_count = sum(1 for item in items if item.decision == "publish_candidate")
        watch_count = sum(1 for item in items if item.decision == "watchlist_waiting_for_answer")
        conflict_count = sum(1 for item in items if item.decision == "conflict_explainer")
        blocked_count = sum(1 for item in items if item.decision == "blocked_high_risk")
        rows.append(
            {
                "game_id": game_id,
                "game_name": top_cluster.game_name,
                "game_type": GAME_TYPE_LABELS.get(game_id, "未分类"),
                "guide_need_score": guide_need_score,
                "top_need": top_cluster.need_key,
                "top_question": top_cluster.representative_question,
                "publish_candidate_count": publish_count,
                "watchlist_count": watch_count,
                "conflict_count": conflict_count,
                "blocked_high_risk_count": blocked_count,
                "reason": _ranking_reason(top_cluster),
            }
        )
    return sorted(rows, key=lambda row: row["guide_need_score"], reverse=True)


def _ranking_reason(cluster: PlayerNeedCluster) -> str:
    if cluster.decision == "publish_candidate":
        return "已有答案且证据成熟，适合优先做成攻略草稿。"
    if cluster.decision == "watchlist_waiting_for_answer":
        return "热度高但答案不成熟，适合进入监控区等待可信答案。"
    if cluster.decision == "conflict_explainer":
        return "答案冲突明显，适合做对比分析和不确定性解释。"
    if cluster.decision == "blocked_high_risk":
        return "风险较高，不能正常推荐，只适合安全提示或阻断。"
    return "当前机会一般，需要更明确的范围或更强证据。"


def _rank_dimension(clusters: list[PlayerNeedCluster], key: str, label: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[PlayerNeedCluster]] = defaultdict(list)
    for cluster in clusters:
        raw_value = getattr(cluster, key)
        value = raw_value.value if hasattr(raw_value, "value") else raw_value
        grouped[str(value)].append(cluster)
    rows = []
    for value, items in grouped.items():
        score = round(sum(_guide_need_score(item) for item in items) / len(items))
        rows.append(
            {
                "label": label,
                "value": value,
                "score": score,
                "topic_count": len(items),
                "top_game": max(items, key=_guide_need_score).game_name,
                "top_need": max(items, key=_guide_need_score).need_key,
            }
        )
    return sorted(rows, key=lambda row: (row["score"], row["topic_count"]), reverse=True)


def _game_heat_ranking_score(game: GameHeatSignal) -> int:
    source_diversity = len(set(game.region_signals))
    source_diversity_score = min(100, source_diversity * 18)
    rank_score = max(0, 100 - game.steam_player_rank) if game.steam_player_rank else 0
    recency_score = max(0, 100 - min(game.update_recency_days, 100)) if game.update_recency_days is not None else 0
    cross_region_score = min(100, game.cross_region_mentions * 20)
    score = round(
        rank_score * 0.2
        + min(game.steam_review_velocity, 100) * 0.2
        + min(game.community_post_velocity, 100) * 0.25
        + recency_score * 0.15
        + cross_region_score * 0.12
        + source_diversity_score * 0.08
    )
    return max(0, min(100, score))


def rank_hot_games(games: list[GameHeatSignal], *, mode: str = "fixture", limit: int = 20) -> list[dict[str, Any]]:
    bounded_limit = max(1, min(limit, 20))
    rows: list[dict[str, Any]] = []
    for game in games:
        scored = score_game_heat(game)
        source_diversity = len(set(scored.region_signals))
        reasons = list(scored.reasons)
        if source_diversity >= 2:
            reasons.append("Multiple source or region signals increase ranking confidence.")
        rows.append(
            {
                "game_id": scored.game_id,
                "game_name": scored.game_name,
                "mode": mode,
                "ranking_score": _game_heat_ranking_score(scored),
                "heat_score": scored.heat_score,
                "steam_player_rank": scored.steam_player_rank,
                "steam_review_velocity": scored.steam_review_velocity,
                "discussion_velocity": scored.community_post_velocity,
                "update_recency_days": scored.update_recency_days,
                "cross_region_mentions": scored.cross_region_mentions,
                "source_diversity": source_diversity,
                "region_signals": scored.region_signals,
                "candidate_only": True,
                "reasons": reasons,
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            row["ranking_score"],
            row["discussion_velocity"],
            -(row["update_recency_days"] or 999),
            row["source_diversity"],
        ),
        reverse=True,
    )[:bounded_limit]


def _cluster_ranking_row(cluster: PlayerNeedCluster) -> dict[str, Any]:
    decision = cluster.decision.value if hasattr(cluster.decision, "value") else cluster.decision
    answer_status = cluster.answer_status.value if hasattr(cluster.answer_status, "value") else cluster.answer_status
    runnable = cluster.recommended_next_action == "send_to_evidence_pipeline" and cluster.risk_level != "high"
    return {
        "cluster_id": cluster.cluster_id,
        "game_id": cluster.game_id,
        "game_name": cluster.game_name,
        "need_key": cluster.need_key,
        "decision": decision,
        "intent": cluster.search_intent,
        "evidence_quality": cluster.evidence_quality,
        "heat": cluster.heat_score,
        "answer_status": answer_status,
        "risk": cluster.risk_level,
        "recommended_next_action": cluster.recommended_next_action,
        "recommended_article_intent": cluster.recommended_article_intent,
        "guide_need_score": _guide_need_score(cluster),
        "content_opportunity_score": cluster.content_opportunity_score,
        "publish_ready": False,
        "runnable": runnable,
        "representative_question": cluster.representative_question,
    }


def rank_hot_question_buckets(clusters: list[PlayerNeedCluster], *, limit: int = 5) -> dict[str, list[dict[str, Any]]]:
    bounded_limit = max(1, min(limit, 20))
    rows = [_cluster_ranking_row(cluster) for cluster in clusters]

    def ordered(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(items, key=lambda row: (row["guide_need_score"], row["heat"], row["evidence_quality"]), reverse=True)[
            :bounded_limit
        ]

    hot_answered = [
        row
        for row in rows
        if row["answer_status"] == "answered" and row["risk"] != "high" and row["decision"] != "blocked_high_risk"
    ]
    hot_unanswered = [
        {**row, "runnable": False}
        for row in rows
        if row["decision"] == "watchlist_waiting_for_answer" or row["answer_status"] in {"unanswered", "unknown"}
    ]
    conflict_topics = [{**row, "runnable": False} for row in rows if row["decision"] == "conflict_explainer"]
    high_risk = [{**row, "runnable": False, "publish_ready": False} for row in rows if row["risk"] == "high"]
    must_check = [
        row
        for row in rows
        if row["decision"] in {"publish_candidate", "conflict_explainer", "watchlist_waiting_for_answer"}
        and row["risk"] != "high"
    ]
    return {
        "hot_answered_questions": ordered(hot_answered),
        "hot_unanswered_watchlist_questions": ordered(hot_unanswered),
        "conflict_answer_topics": ordered(conflict_topics),
        "high_risk_blocked_topics": ordered(high_risk),
        "must_check_guide_topics": ordered(must_check),
    }


def hot_strategy_rankings(limit: int = 5) -> dict[str, Any]:
    result = search_player_needs(DiscoverySearchRequest(limit=100))
    clusters = result.clusters
    hot_games_top_20 = rank_hot_games(result.game_candidates, mode=result.mode, limit=20)
    question_buckets = rank_hot_question_buckets(clusters, limit=limit)
    games = _game_summary(clusters)[:limit]

    audience_rows = []
    for profile_id, profile in AUDIENCE_PROFILES.items():
        ranked = sorted(
            (
                {
                    "profile_id": profile_id,
                    "profile_label": profile["label"],
                    "profile_description": profile["description"],
                    "game_name": cluster.game_name,
                    "need_key": cluster.need_key,
                    "score": _audience_scores(cluster)[profile_id],
                    "decision": cluster.decision.value if hasattr(cluster.decision, "value") else cluster.decision,
                    "representative_question": cluster.representative_question,
                }
                for cluster in clusters
            ),
            key=lambda row: row["score"],
            reverse=True,
        )
        audience_rows.extend(ranked[:3])

    cluster_rows = sorted(
        [
            {
                "game_name": cluster.game_name,
                "need_key": cluster.need_key,
                "decision": cluster.decision.value if hasattr(cluster.decision, "value") else cluster.decision,
                "guide_need_score": _guide_need_score(cluster),
                "content_opportunity_score": cluster.content_opportunity_score,
                "heat_score": cluster.heat_score,
                "evidence_quality": cluster.evidence_quality,
                "risk_level": cluster.risk_level,
                "representative_question": cluster.representative_question,
            }
            for cluster in clusters
        ],
        key=lambda row: row["guide_need_score"],
        reverse=True,
    )[:limit]

    return {
        "status": "completed",
        "mode": result.mode,
        "real_collection_performed": result.real_collection_performed,
        "publish_ready": False,
        "publishing_performed": False,
        "real_market_hot_games_top_5": hot_games_top_20[:5],
        "real_market_hot_games_top_20": hot_games_top_20,
        "question_ranking_buckets": question_buckets,
        "methodology": "攻略需求分 = 热度、内容机会、可执行性、证据质量、跨地区信号、答案状态和风险惩罚的综合分。性别相关榜单是兴趣画像向，不是对真实玩家性别做判断。",
        "top_hot_games": games,
        "top_guide_needs": cluster_rows,
        "audience_rankings": audience_rows,
        "game_type_rankings": _rank_dimension(clusters, "search_intent", "问题类型"),
        "decision_rankings": _rank_dimension(clusters, "decision", "漏斗结论"),
    }
