from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Iterable, Literal

from packages.discovery.fixtures import load_discovery_fixtures
from packages.discovery.scoring import (
    actionability_score_for,
    answer_status_for,
    classify_competition_gap,
    classify_topic_actionability,
    classify_topic_lifecycle,
    content_opportunity_score_for,
    decision_for,
    question_heat_score,
    score_game_heat,
)
from packages.shared.schemas import (
    AnswerStatus,
    DiscoveryArticleCandidate,
    DiscoveryDecision,
    DiscoveryRetrospectiveReport,
    DiscoverySearchRequest,
    DiscoverySearchResponse,
    DiscoveryWatchlistItem,
    GameHeatSignal,
    PlayerNeedCluster,
    PlayerQuestionSignal,
)

SEARCH_INTENT_BY_NEED_KEY: dict[str, str] = {
    "crash_after_update": "bug_fix",
    "controller_input_issue": "bug_fix",
    "save_file_location": "save_file",
    "save_recovery_risk": "save_file",
    "settings_steam_deck": "settings",
    "build_loadout": "build",
    "quest_route": "quest_blocker",
    "hidden_item": "hidden_item",
    "map_exploration_route": "map_exploration",
    "general_player_question": "walkthrough",
}

MULTILINGUAL_TOPIC_HINTS: dict[str, list[str]] = {
    "save": ["save", "savedata", "save data", "セーブ", "セーブデータ", "저장", "세이브"],
    "location": ["location", "where", "場所", "どこ", "위치", "어디"],
    "bug": ["crash", "black screen", "bug", "error", "freeze", "クラッシュ", "エラー", "버그", "오류", "멈춤"],
    "settings": ["settings", "fps", "performance", "graphics", "設定", "설정"],
    "map": ["map", "route", "exploration", "マップ", "地図", "지도", "루트"],
    "quest": ["quest", "npc", "objective", "mission", "クエスト", "퀘스트"],
    "hidden": ["hidden", "secret", "collectible", "隠し", "秘密", "숨겨진", "비밀"],
}

PLANNED_TOPIC_SOURCE_TYPES = [
    "steam_discussion",
    "reddit",
    "discord_forum",
    "official_forum",
    "wiki_comment",
    "jp_community",
    "kr_community",
    "serp_snippet",
]


def search_intent_for_need_key(
    need_key: str,
) -> Literal[
    "bug_fix",
    "location",
    "walkthrough",
    "build",
    "settings",
    "compatibility",
    "save_file",
    "map_exploration",
    "hidden_item",
    "quest_blocker",
]:
    return SEARCH_INTENT_BY_NEED_KEY.get(need_key, "walkthrough")  # type: ignore[return-value]


def _contains_any(haystack: str, terms: list[str]) -> bool:
    return any(term.lower() in haystack for term in terms)


def normalization_hints_for_question(text: str, tags: list[str]) -> list[str]:
    haystack = f"{text} {' '.join(tags)}".lower()
    hints = [name for name, terms in MULTILINGUAL_TOPIC_HINTS.items() if _contains_any(haystack, terms)]
    return hints

def _need_key(text: str, tags: list[str]) -> str:
    haystack = f"{text} {' '.join(tags)}".lower()
    hints = set(normalization_hints_for_question(text, tags))
    if "save" in hints:
        if any(term in haystack for term in ["tool", "recovery"]):
            return "save_recovery_risk"
        return "save_file_location"
    if "bug" in hints or "patch" in haystack:
        return "crash_after_update"
    if "steam deck" in haystack or "proton" in haystack or "settings" in hints:
        return "settings_steam_deck"
    if any(term in haystack for term in ["build", "weapon", "loadout", "skill tree"]):
        return "build_loadout"
    if "controller" in haystack:
        return "controller_input_issue"
    if "quest" in hints:
        return "quest_route"
    if "hidden" in hints:
        return "hidden_item"
    if "map" in hints or any(term in haystack for term in ["bench", "room"]):
        return "map_exploration_route"
    return "general_player_question"


def _question_quality(question: PlayerQuestionSignal, game_heat: int) -> tuple[int, int, int, int]:
    english_bonus = 1 if question.source_region == "en" or question.language == "en" else 0
    return (
        question_heat_score(question, game_heat),
        question.evidence_quality,
        english_bonus,
        len(question.question_text),
    )


def region_signal_summary_for(questions: Iterable[PlayerQuestionSignal]) -> dict[str, object]:
    items = list(questions)
    by_region = Counter(item.source_region for item in items)
    by_language = Counter((item.language or item.source_region or "unknown") for item in items)
    duplicate_by_region: dict[str, int] = defaultdict(int)
    for item in items:
        duplicate_by_region[item.source_region] += item.duplicate_count
    regions = sorted(by_region)
    return {
        "regions": regions,
        "region_counts": dict(sorted(by_region.items())),
        "language_counts": dict(sorted(by_language.items())),
        "duplicate_count_by_region": dict(sorted(duplicate_by_region.items())),
        "cross_region_repeat": len(regions) >= 2,
        "language_gap_opportunity": len(regions) >= 2 and ("en" in regions) and any(region in {"jp", "kr"} for region in regions),
    }


def region_signal_score_for(summary: dict[str, object]) -> int:
    regions = summary.get("regions", [])
    region_count = len(regions) if isinstance(regions, list) else 0
    duplicate_by_region = summary.get("duplicate_count_by_region", {})
    duplicate_total = sum(duplicate_by_region.values()) if isinstance(duplicate_by_region, dict) else 0
    cross_region_bonus = 25 if summary.get("cross_region_repeat") else 0
    language_gap_bonus = 20 if summary.get("language_gap_opportunity") else 0
    return min(100, region_count * 18 + min(duplicate_total * 2, 35) + cross_region_bonus + language_gap_bonus)


def source_coverage_for(source_types: list[str], source_regions: list[str]) -> dict[str, object]:
    current = sorted(source_types)
    missing = [source_type for source_type in PLANNED_TOPIC_SOURCE_TYPES if source_type not in current]
    regional_gaps = [region for region in ["jp", "kr"] if region not in source_regions]
    coverage_ratio = round(len(current) / len(PLANNED_TOPIC_SOURCE_TYPES), 2)
    if len(current) >= 3 and not regional_gaps:
        coverage_level = "broad"
    elif len(current) >= 2 or not regional_gaps:
        coverage_level = "partial"
    else:
        coverage_level = "thin"
    return {
        "current_source_types": current,
        "planned_source_types": PLANNED_TOPIC_SOURCE_TYPES,
        "missing_source_types": missing,
        "source_type_diversity_count": len(current),
        "source_region_diversity_count": len(source_regions),
        "regional_gaps": regional_gaps,
        "coverage_ratio": coverage_ratio,
        "coverage_level": coverage_level,
        "real_collection_performed": False,
    }


def _risk_for(questions: Iterable[PlayerQuestionSignal]) -> str:
    risks = {item.risk_level for item in questions}
    if "high" in risks:
        return "high"
    if "medium" in risks:
        return "medium"
    return "low"


def _article_intent(game_name: str, need_key: str, answer_status: AnswerStatus) -> str:
    if need_key == "save_file_location":
        return f"Help players find and safely back up {game_name} save files."
    if need_key == "crash_after_update":
        if answer_status == AnswerStatus.unanswered:
            return f"Monitor {game_name} crash reports until a source-backed fix appears."
        return f"Help players troubleshoot {game_name} crash reports with low-risk steps first."
    if need_key == "controller_input_issue":
        return f"Explain competing {game_name} controller fixes and rank low-risk checks."
    if need_key == "map_exploration_route":
        return f"Help players navigate a {game_name} exploration route without copying maps."
    if need_key == "save_recovery_risk":
        return f"Warn players about risky {game_name} save recovery claims and safer alternatives."
    if need_key == "settings_steam_deck":
        return f"Help players choose safe {game_name} settings before risky tweaks."
    if need_key == "build_loadout":
        return f"Help players compare {game_name} build options with source-backed tradeoffs."
    if need_key == "quest_route":
        return f"Help players follow a {game_name} quest route without spoilers beyond the asked step."
    if need_key == "hidden_item":
        return f"Help players find a {game_name} hidden item with source-traced steps."
    return f"Clarify a recurring {game_name} player question."


def piko_value_add_for_decision(
    decision: DiscoveryDecision,
    cross_language: bool,
    competition_gap_status: str = "weak",
    actionability_label: str = "needs_more_sources",
) -> list[str]:
    values = {
        DiscoveryDecision.publish_candidate: [
            "Single-page clarity: combine scattered answers into one source-traced guide.",
            "Risk ordering: rank low-risk steps before risky actions.",
        ],
        DiscoveryDecision.watchlist_waiting_for_answer: [
            "Monitoring value: track a hot unresolved issue until a credible answer appears.",
        ],
        DiscoveryDecision.conflict_explainer: [
            "Conflict explanation: explain competing answers instead of pretending there is one answer.",
        ],
        DiscoveryDecision.evergreen_candidate: [
            "Evergreen utility: create long-lived reference content from repeated questions.",
        ],
        DiscoveryDecision.rising_opportunity: [
            "Freshness value: catch a fast-rising player need before strong guides exist.",
        ],
        DiscoveryDecision.blocked_high_risk: [
            "Risk warning: redirect players away from unsafe tools or destructive fixes.",
        ],
        DiscoveryDecision.insufficient_evidence: [
            "Evidence discipline: keep weak claims out of drafting until better sources exist.",
        ],
        DiscoveryDecision.ignore: ["Low current content value."],
    }[decision]
    if decision == DiscoveryDecision.ignore:
        return values
    if cross_language:
        values.append("Cross-language bridge: connect repeated EN/JP/KR questions with clear sourcing.")
    if competition_gap_status in {"fragmented", "stale", "absent"}:
        values.append(f"Gap fill: existing material appears {competition_gap_status}.")
    if actionability_label == "single_page_answerable":
        values.append("Focused scope: this topic can likely be answered on one useful page.")
    return values


def source_search_hints_for_cluster(cluster: PlayerNeedCluster) -> list[str]:
    hints = [
        f"{cluster.game_name} {cluster.need_key.replace('_', ' ')}",
        f"{cluster.game_name} {cluster.representative_question}",
    ]
    for region in cluster.source_regions:
        hints.append(f"{cluster.game_name} {cluster.need_key.replace('_', ' ')} {region}")
    for source_type in cluster.source_types:
        hints.append(f"{cluster.game_name} {cluster.need_key.replace('_', ' ')} {source_type}")
    return hints[:6]


def recommended_next_action_for(decision: DiscoveryDecision) -> str:
    return {
        DiscoveryDecision.publish_candidate: "send_to_evidence_pipeline",
        DiscoveryDecision.watchlist_waiting_for_answer: "add_to_watchlist",
        DiscoveryDecision.conflict_explainer: "prepare_conflict_brief",
        DiscoveryDecision.evergreen_candidate: "queue_evergreen_evidence_review",
        DiscoveryDecision.rising_opportunity: "monitor_and_collect_evidence",
        DiscoveryDecision.blocked_high_risk: "block_publish_and_prepare_safety_note",
        DiscoveryDecision.insufficient_evidence: "collect_more_evidence",
        DiscoveryDecision.ignore: "no_action",
    }[decision]


def safety_notes_for(decision: DiscoveryDecision, risk_level: str) -> list[str]:
    notes = ["Discovery output is candidate-only and is not publishing permission."]
    if risk_level == "high" or decision == DiscoveryDecision.blocked_high_risk:
        notes.append("High-risk player advice must not become a normal guide recommendation.")
    if decision == DiscoveryDecision.watchlist_waiting_for_answer:
        notes.append("Wait for a credible answer before article drafting.")
    return notes


WATCHLIST_STATE_TRANSITIONS = {
    "watching": "answer_seen when accepted/official/high-quality answer signal appears; stale when freshness and heat fade.",
    "answer_seen": "evidence_ready when evidence quality reaches the threshold for pipeline review.",
    "evidence_ready": "closed after a candidate is handed to evidence pipeline or manually dismissed.",
    "stale": "closed if the topic stays low-value; watching if fresh signals return.",
    "closed": "terminal unless operator reopens the topic.",
}


def watchlist_state_for_signal(signal: PlayerQuestionSignal, freshness_score: int = 0, heat_score: int = 0) -> str:
    if signal.has_accepted_answer or signal.has_official_answer:
        if signal.evidence_quality >= 60:
            return "evidence_ready"
        return "answer_seen"
    if signal.evidence_quality >= 70:
        return "evidence_ready"
    if freshness_score <= 20 and heat_score < 45:
        return "stale"
    return "watching"


def watchlist_refresh_plan_for(cluster: PlayerNeedCluster) -> tuple[int, str]:
    if cluster.topic_lifecycle == "rising" or cluster.freshness_score >= 75 or cluster.urgency_score >= 80:
        return 6, "High-growth unresolved topic; check frequently for credible answers."
    if cluster.topic_lifecycle == "new" or cluster.freshness_score >= 55:
        return 12, "Fresh topic; check for answer maturity soon."
    if cluster.topic_lifecycle == "stale":
        return 72, "Low-freshness topic; reduce refresh pressure unless new signals appear."
    return 24, "Routine watchlist refresh for answer or evidence maturity."


def _average_score(values: Iterable[int]) -> int:
    items = list(values)
    if not items:
        return 0
    return round(sum(items) / len(items))


def _freshness_score(game: GameHeatSignal, questions: Iterable[PlayerQuestionSignal]) -> int:
    items = list(questions)
    growth = max((item.growth_24h for item in items), default=0)
    patch_bonus = 15 if any("patch" in item.tags for item in items) else 0
    update_score = 0 if game.update_recency_days is None else max(0, 100 - min(game.update_recency_days, 100))
    return max(0, min(100, round(0.55 * min(growth, 100) + 0.3 * update_score + patch_bonus)))


def _evergreen_value(questions: Iterable[PlayerQuestionSignal], cross_language: bool) -> int:
    items = list(questions)
    if any("evergreen" in item.tags or "location" in item.tags for item in items):
        return 85
    if cross_language:
        return 65
    return 30


def _cluster_questions(
    games_by_id: dict[str, GameHeatSignal],
    questions: list[PlayerQuestionSignal],
) -> list[PlayerNeedCluster]:
    grouped: dict[tuple[str, str], list[PlayerQuestionSignal]] = defaultdict(list)
    for question in questions:
        grouped[(question.game_id, _need_key(question.question_text, question.tags))].append(question)

    clusters: list[PlayerNeedCluster] = []
    for (game_id, need_key), items in grouped.items():
        game = games_by_id[game_id]
        heat_scores = [question_heat_score(item, game.heat_score) for item in items]
        frequency_score = min(100, sum(item.duplicate_count for item in items) * 9 + len(items) * 8)
        urgency_score = min(100, max(item.growth_24h for item in items) + (15 if any("patch" in item.tags for item in items) else 0))
        evidence_quality = round(sum(item.evidence_quality for item in items) / len(items))
        heat_score = max(heat_scores)
        risk_level = _risk_for(items)
        answer_status = answer_status_for(items)
        growth_score = max(item.growth_24h for item in items)
        evergreen = any("evergreen" in item.tags or "location" in item.tags for item in items)
        cross_language = len({item.source_region for item in items}) >= 2 or any("cross_language" in item.tags for item in items)
        conflict_score = min(100, sum(item.answer_conflict_count for item in items) * 35)
        freshness_score = _freshness_score(game, items)
        evergreen_score = _evergreen_value(items, cross_language)
        competition_gap = _average_score(item.competition_gap for item in items)
        piko_value_add_score = _average_score(item.piko_value_add_score for item in items)
        actionability_label, actionability_reasons = classify_topic_actionability(
            need_key,
            answer_status,
            risk_level,
            evidence_quality,
        )
        actionability_score = actionability_score_for(actionability_label)
        topic_lifecycle = classify_topic_lifecycle(
            answer_status,
            heat_score,
            growth_score,
            freshness_score,
            evidence_quality,
            evergreen_score,
        )
        decision = decision_for(
            answer_status,
            heat_score,
            evidence_quality,
            risk_level,
            growth_score,
            evergreen,
            cross_language,
            freshness_score=freshness_score,
            competition_gap=competition_gap,
            piko_value_add_score=piko_value_add_score,
        )
        question_ids = [item.question_id for item in items]
        source_types = sorted({item.source_type for item in items})
        source_regions = sorted({item.source_region for item in items})
        region_signal_summary = region_signal_summary_for(items)
        region_signal_score = region_signal_score_for(region_signal_summary)
        source_coverage = source_coverage_for(source_types, source_regions)
        competition_gap_status = classify_competition_gap(
            competition_gap,
            str(source_coverage["coverage_level"]),
            freshness_score,
        )
        content_opportunity_score, content_opportunity_reasons = content_opportunity_score_for(
            decision,
            heat_score,
            answer_status,
            evidence_quality,
            risk_level,
            actionability_score,
            competition_gap,
            piko_value_add_score,
        )
        representative = max(items, key=lambda item: _question_quality(item, game.heat_score))
        normalization_hints = sorted(
            {
                hint
                for item in items
                for hint in normalization_hints_for_question(item.question_text, item.tags)
            }
        )
        source_diversity_count = len(source_types) + len(source_regions)
        duplicate_count = sum(item.duplicate_count for item in items)
        reasons = [
            f"Game heat score: {game.heat_score}.",
            f"Question heat score: {heat_score}.",
            f"Answer status: {answer_status.value}.",
            f"Evidence quality: {evidence_quality}.",
            f"Competition gap: {competition_gap}.",
            f"Piko value add score: {piko_value_add_score}.",
        ]
        if answer_status == AnswerStatus.unanswered:
            reasons.append("No accepted or official answer is present yet.")
        if answer_status == AnswerStatus.conflicting:
            reasons.append("Community answers conflict and need synthesis.")
        if risk_level == "high":
            reasons.append("High-risk actions require blocking or safety framing.")
        if region_signal_summary["cross_region_repeat"]:
            reasons.append("Repeated questions appear across multiple regions.")
        if region_signal_summary["language_gap_opportunity"]:
            reasons.append("Language-gap opportunity: bridge EN and JP/KR signals with clear sourcing.")
        reasons.append(f"Source coverage level: {source_coverage['coverage_level']}.")
        reasons.append(f"Competition gap status: {competition_gap_status}.")
        clusters.append(
            PlayerNeedCluster(
                cluster_id=f"{game_id}:{need_key}",
                game_id=game_id,
                game_name=game.game_name,
                need_key=need_key,
                search_intent=search_intent_for_need_key(need_key),
                normalization_hints=normalization_hints,
                representative_question=representative.question_text,
                representative_question_id=representative.question_id,
                representative_questions=[item.question_text for item in items[:5]],
                source_types=source_types,
                source_regions=source_regions,
                source_diversity_count=source_diversity_count,
                region_signal_summary=region_signal_summary,
                region_signal_score=region_signal_score,
                cross_region_repeat=bool(region_signal_summary["cross_region_repeat"]),
                language_gap_opportunity=bool(region_signal_summary["language_gap_opportunity"]),
                source_coverage=source_coverage,
                duplicate_count=duplicate_count,
                question_ids=question_ids,
                heat_score=heat_score,
                frequency_score=frequency_score,
                urgency_score=urgency_score,
                evidence_quality=evidence_quality,
                freshness_score=freshness_score,
                conflict_score=conflict_score,
                evergreen_value=evergreen_score,
                competition_gap=competition_gap,
                competition_gap_status=competition_gap_status,
                actionability_score=actionability_score,
                piko_value_add_score=piko_value_add_score,
                content_opportunity_score=content_opportunity_score,
                content_opportunity_reasons=content_opportunity_reasons,
                risk_level=risk_level,  # type: ignore[arg-type]
                answer_status=answer_status,
                topic_lifecycle=topic_lifecycle,
                actionability_label=actionability_label,
                actionability_reasons=actionability_reasons,
                decision=decision,
                recommended_article_intent=_article_intent(game.game_name, need_key, answer_status),
                monitor_reason="Wait for a credible answer or official reply." if decision == DiscoveryDecision.watchlist_waiting_for_answer else None,
                piko_value_add=piko_value_add_for_decision(
                    decision,
                    cross_language,
                    competition_gap_status,
                    actionability_label,
                ),
                score_inputs={
                    "game_heat": game.heat_score,
                    "question_heat": heat_score,
                    "answer_status": answer_status.value,
                    "evidence_quality": evidence_quality,
                    "conflict_score": conflict_score,
                    "risk_level": risk_level,
                    "freshness_score": freshness_score,
                    "evergreen_value": evergreen_score,
                    "competition_gap": competition_gap,
                    "competition_gap_status": competition_gap_status,
                    "actionability_score": actionability_score,
                    "piko_value_add_score": piko_value_add_score,
                    "content_opportunity_score": content_opportunity_score,
                },
                topic_score_components={
                    "topic_heat": heat_score,
                    "urgency": urgency_score,
                    "evidence_maturity": evidence_quality,
                    "conflict_level": conflict_score,
                    "risk_level": risk_level,
                    "freshness": freshness_score,
                    "evergreen_value": evergreen_score,
                    "competition_gap": competition_gap,
                    "actionability": actionability_score,
                    "piko_value_add": piko_value_add_score,
                    "content_opportunity": content_opportunity_score,
                },
                recommended_next_action=recommended_next_action_for(decision),
                safety_notes=safety_notes_for(decision, risk_level),
                reasons=reasons,
            )
        )
        clusters[-1].source_search_hints = source_search_hints_for_cluster(clusters[-1])
    return clusters


def _matches_query(cluster: PlayerNeedCluster, query: str | None) -> bool:
    if not query:
        return True
    haystack = " ".join(
        [
            cluster.game_name,
            cluster.need_key.replace("_", " "),
            cluster.representative_question,
            " ".join(cluster.representative_questions),
        ]
    ).lower()
    terms = [term for term in query.lower().split() if term]
    return all(term in haystack for term in terms)


def search_player_needs(request: DiscoverySearchRequest | None = None) -> DiscoverySearchResponse:
    request = request or DiscoverySearchRequest()
    raw_games, questions = load_discovery_fixtures()
    games = [score_game_heat(game) for game in raw_games]
    games_by_id = {game.game_id: game for game in games}
    clusters = _cluster_questions(games_by_id, questions)

    filtered_games = [game for game in games if game.heat_score >= request.min_game_heat]
    allowed_game_ids = {game.game_id for game in filtered_games}
    clusters = [
        cluster
        for cluster in clusters
        if cluster.game_id in allowed_game_ids
        and cluster.heat_score >= request.min_question_heat
        and cluster.content_opportunity_score >= request.min_content_opportunity_score
        and (not request.game_name or request.game_name.lower() in cluster.game_name.lower())
        and _matches_query(cluster, request.query)
        and (not request.regions or any(region in request.regions for region in cluster.source_regions))
        and (not request.source_types or any(source_type in request.source_types for source_type in cluster.source_types))
        and (not request.search_intents or cluster.search_intent in request.search_intents)
        and (not request.topic_lifecycles or cluster.topic_lifecycle in request.topic_lifecycles)
        and (not request.actionability_labels or cluster.actionability_label in request.actionability_labels)
        and (not request.answer_statuses or cluster.answer_status in request.answer_statuses)
        and (not request.decisions or cluster.decision in request.decisions)
    ]
    clusters.sort(
        key=lambda cluster: (
            cluster.content_opportunity_score,
            cluster.decision == DiscoveryDecision.publish_candidate,
            cluster.urgency_score,
            cluster.evidence_quality,
        ),
        reverse=True,
    )
    clusters = clusters[: request.limit]
    counts = Counter(cluster.decision.value for cluster in clusters)
    return DiscoverySearchResponse(
        game_candidates=sorted(filtered_games, key=lambda game: game.heat_score, reverse=True),
        clusters=clusters,
        funnel_counts=dict(counts),
        real_collection_performed=False,
        next_actions=[
            "Send publish_candidate clusters into the article pipeline.",
            "Put watchlist_waiting_for_answer clusters into monitoring.",
            "Use conflict_explainer clusters for synthesis pages that explain uncertainty.",
            f"Generated from fixture search at {datetime.now(timezone.utc).isoformat()}.",
        ],
    )


def watchlist_items_from_clusters(clusters: list[PlayerNeedCluster]) -> list[DiscoveryWatchlistItem]:
    items: list[DiscoveryWatchlistItem] = []
    for cluster in clusters:
        if cluster.decision != DiscoveryDecision.watchlist_waiting_for_answer:
            continue
        refresh_interval_hours, next_check_reason = watchlist_refresh_plan_for(cluster)
        items.append(
            DiscoveryWatchlistItem(
                watchlist_id=f"watch_{cluster.cluster_id.replace(':', '_')}",
                cluster_id=cluster.cluster_id,
                game_name=cluster.game_name,
                player_question=cluster.representative_question,
                reason=cluster.monitor_reason or "Waiting for credible evidence.",
                state="watching",
                refresh_interval_hours=refresh_interval_hours,
                next_check_reason=next_check_reason,
                trigger_conditions=[
                    "official_reply",
                    "accepted_answer",
                    "high_upvote_answer",
                    "wiki_update",
                    "patch_notes_update",
                    "cross_language_answer",
                ],
                promotion_triggers=[
                    "accepted_answer",
                    "official_answer",
                    "evidence_quality>=60",
                ],
                state_transitions=WATCHLIST_STATE_TRANSITIONS,
                last_seen_signals={
                    "heat_score": cluster.heat_score,
                    "freshness_score": cluster.freshness_score,
                    "topic_lifecycle": cluster.topic_lifecycle,
                    "content_opportunity_score": cluster.content_opportunity_score,
                    "source_regions": cluster.source_regions,
                },
            )
        )
    return items


def article_candidate_from_cluster(cluster: PlayerNeedCluster) -> DiscoveryArticleCandidate:
    candidate_type_by_decision = {
        DiscoveryDecision.publish_candidate: "solution_candidate",
        DiscoveryDecision.conflict_explainer: "synthesis_candidate",
        DiscoveryDecision.evergreen_candidate: "solution_candidate",
        DiscoveryDecision.rising_opportunity: "monitoring_candidate",
        DiscoveryDecision.watchlist_waiting_for_answer: "watchlist_only",
        DiscoveryDecision.blocked_high_risk: "blocked_safety_note",
        DiscoveryDecision.insufficient_evidence: "evidence_gap_candidate",
        DiscoveryDecision.ignore: "ignored",
    }
    runnable_decisions = {
        DiscoveryDecision.publish_candidate,
        DiscoveryDecision.conflict_explainer,
        DiscoveryDecision.evergreen_candidate,
    }
    runnable = cluster.decision in runnable_decisions and cluster.risk_level != "high"
    risk_flags = []
    if cluster.risk_level != "low":
        risk_flags.append(f"risk_level:{cluster.risk_level}")
    if cluster.answer_status == AnswerStatus.conflicting:
        risk_flags.append("conflicting_answers")
    if cluster.answer_status == AnswerStatus.unanswered:
        risk_flags.append("no_credible_answer_yet")

    safety_flags = ["candidate_only", "requires_evidence_pipeline", "not_publish_ready"]
    safety_reasons = ["Discovery candidates are not publishing approval."]
    if not runnable:
        safety_flags.append("not_runnable")
        safety_reasons.append("This discovery decision cannot be sent directly to article drafting.")
    if cluster.decision == DiscoveryDecision.conflict_explainer:
        safety_flags.append("synthesis_only")
        safety_reasons.append("Conflicting answers require synthesis and uncertainty framing, not a normal solution article.")
    if cluster.decision == DiscoveryDecision.watchlist_waiting_for_answer:
        safety_flags.append("watchlist_only")
        safety_reasons.append("Wait for an accepted, official, or otherwise credible answer before drafting.")
    if cluster.decision == DiscoveryDecision.blocked_high_risk or cluster.risk_level == "high":
        safety_flags.append("high_risk_block")
        safety_reasons.append("High-risk player advice must be blocked from normal guide generation.")

    hints = cluster.source_search_hints
    return DiscoveryArticleCandidate(
        candidate_id=f"candidate_{cluster.cluster_id.replace(':', '_')}",
        cluster_id=cluster.cluster_id,
        game_id=cluster.game_id,
        game_name=cluster.game_name,
        need_key=cluster.need_key,
        search_intent=cluster.search_intent,
        normalization_hints=cluster.normalization_hints,
        player_question=cluster.representative_question,
        article_intent=cluster.recommended_article_intent,
        decision=cluster.decision,
        answer_status=cluster.answer_status,
        risk_level=cluster.risk_level,
        candidate_type=candidate_type_by_decision[cluster.decision],  # type: ignore[arg-type]
        runnable=runnable,
        source_search_hints=hints,
        source_query_hints=hints,
        required_source_types=cluster.source_types,
        preferred_source_types=cluster.source_types,
        source_regions=cluster.source_regions,
        risk_flags=risk_flags,
        safety_flags=safety_flags,
        safety_reasons=safety_reasons,
        piko_value_add=cluster.piko_value_add,
        cluster_reasons=cluster.reasons,
        score_inputs=cluster.score_inputs,
        publish_ready=False,
        requires_evidence_pipeline=True,
        safety_notes=safety_notes_for(cluster.decision, cluster.risk_level)
        + ([] if runnable else ["This discovery cluster must not be sent to drafting as article-ready."]),
    )


def article_candidates_from_clusters(clusters: list[PlayerNeedCluster]) -> list[DiscoveryArticleCandidate]:
    return [article_candidate_from_cluster(cluster) for cluster in clusters]


def select_publish_article_candidates(request: DiscoverySearchRequest | None = None) -> list[DiscoveryArticleCandidate]:
    response = search_player_needs(request or DiscoverySearchRequest(limit=20))
    candidates = []
    for cluster in response.clusters:
        if cluster.decision != DiscoveryDecision.publish_candidate:
            continue
        candidate = article_candidate_from_cluster(cluster)
        if candidate.runnable and not candidate.publish_ready and candidate.requires_evidence_pipeline:
            candidates.append(candidate)
    return candidates


def discovery_retrospective_report(clusters: list[PlayerNeedCluster]) -> DiscoveryRetrospectiveReport:
    counts = Counter(cluster.decision.value for cluster in clusters)
    weak_sources = [cluster.cluster_id for cluster in clusters if cluster.evidence_quality < 45]
    return DiscoveryRetrospectiveReport(
        decision_counts=dict(counts),
        publish_candidate_count=counts.get(DiscoveryDecision.publish_candidate.value, 0),
        watchlist_count=counts.get(DiscoveryDecision.watchlist_waiting_for_answer.value, 0),
        blocked_high_risk_count=counts.get(DiscoveryDecision.blocked_high_risk.value, 0),
        weak_source_count=len(weak_sources),
        recommendations=[
            "Review publish candidates through the evidence pipeline before drafting.",
            "Monitor watchlist clusters for accepted or official answers.",
            "Keep high-risk clusters blocked from normal publishing.",
            "Improve weak source clusters with higher-trust source types.",
        ],
        real_collection_performed=False,
    )


def promotion_candidate_from_watchlist(item: DiscoveryWatchlistItem, new_signal: PlayerQuestionSignal) -> dict[str, object]:
    next_state = watchlist_state_for_signal(
        new_signal,
        freshness_score=int(item.last_seen_signals.get("freshness_score", 0)),
        heat_score=int(item.last_seen_signals.get("heat_score", 0)),
    )
    promoted = next_state == "evidence_ready"
    return {
        "watchlist_id": item.watchlist_id,
        "previous_state": item.state,
        "next_state": next_state,
        "promoted": promoted,
        "recommended_next_action": "send_to_evidence_pipeline" if promoted else "keep_watching",
        "triggered_by": {
            "question_id": new_signal.question_id,
            "has_accepted_answer": new_signal.has_accepted_answer,
            "has_official_answer": new_signal.has_official_answer,
            "evidence_quality": new_signal.evidence_quality,
        },
        "publish_ready": False,
        "requires_evidence_pipeline": True,
        "publishing_performed": False,
    }
