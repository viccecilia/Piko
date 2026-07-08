from collections.abc import Iterable

from typing import Literal

from packages.shared.schemas import AnswerStatus, DiscoveryDecision, GameHeatSignal, PlayerQuestionSignal


DISCOVERY_SCORE_INPUTS = [
    "game_heat",
    "question_heat",
    "answer_status",
    "evidence_quality",
    "conflict_score",
    "risk_level",
    "freshness_score",
    "evergreen_value",
    "competition_gap",
    "actionability_score",
    "piko_value_add_score",
]


def clamp_score(value: int | float) -> int:
    return max(0, min(100, round(value)))


def score_game_heat(signal: GameHeatSignal) -> GameHeatSignal:
    rank_score = 0
    if signal.steam_player_rank:
        rank_score = max(0, 100 - signal.steam_player_rank)
    update_score = 0
    if signal.update_recency_days is not None:
        update_score = max(0, 100 - min(signal.update_recency_days, 100))
    cross_region_score = min(100, signal.cross_region_mentions * 20)
    heat = round(
        0.28 * rank_score
        + 0.25 * min(signal.steam_review_velocity, 100)
        + 0.27 * min(signal.community_post_velocity, 100)
        + 0.12 * update_score
        + 0.08 * cross_region_score
    )
    reasons: list[str] = []
    if rank_score >= 70:
        reasons.append("Strong Steam player rank signal.")
    if signal.community_post_velocity >= 70:
        reasons.append("Community discussion velocity is high.")
    if signal.update_recency_days is not None and signal.update_recency_days <= 14:
        reasons.append("Recent update can create fresh player needs.")
    if signal.cross_region_mentions >= 3:
        reasons.append("Multiple regions show discussion activity.")
    return signal.model_copy(update={"heat_score": clamp_score(heat), "reasons": reasons})


def question_heat_score(question: PlayerQuestionSignal, game_heat: int) -> int:
    engagement = min(question.engagement_count, 300) / 300 * 100
    replies = min(question.reply_count, 80) / 80 * 100
    duplicates = min(question.duplicate_count, 12) / 12 * 100
    growth = min(question.growth_24h, 100)
    score = round(0.25 * game_heat + 0.25 * engagement + 0.18 * replies + 0.2 * duplicates + 0.12 * growth)
    return clamp_score(score)


def answer_status_for(questions: Iterable[PlayerQuestionSignal]) -> AnswerStatus:
    items = list(questions)
    if any(item.answer_conflict_count > 0 for item in items):
        return AnswerStatus.conflicting
    if any(item.has_accepted_answer or item.has_official_answer for item in items):
        return AnswerStatus.answered
    if items and max(item.evidence_quality for item in items) >= 45:
        return AnswerStatus.partial
    if items:
        return AnswerStatus.unanswered
    return AnswerStatus.unknown


def decision_for(
    answer_status: AnswerStatus,
    heat_score: int,
    evidence_quality: int,
    risk_level: str,
    growth_score: int,
    evergreen: bool,
    cross_language: bool,
    freshness_score: int = 0,
    competition_gap: int = 50,
    piko_value_add_score: int = 50,
) -> DiscoveryDecision:
    if risk_level == "high":
        return DiscoveryDecision.blocked_high_risk
    if answer_status == AnswerStatus.conflicting and heat_score >= 55:
        return DiscoveryDecision.conflict_explainer
    if answer_status == AnswerStatus.unanswered and heat_score >= 60:
        return DiscoveryDecision.watchlist_waiting_for_answer
    if answer_status == AnswerStatus.answered and heat_score >= 50 and evidence_quality >= 60 and piko_value_add_score >= 40:
        return DiscoveryDecision.publish_candidate
    if (growth_score >= 70 or freshness_score >= 75) and heat_score >= 55:
        return DiscoveryDecision.rising_opportunity
    if evergreen and evidence_quality >= 55:
        return DiscoveryDecision.evergreen_candidate
    if (cross_language or competition_gap >= 65) and evidence_quality >= 55:
        return DiscoveryDecision.evergreen_candidate
    if evidence_quality < 45:
        return DiscoveryDecision.insufficient_evidence
    return DiscoveryDecision.ignore


def actionability_score_for(label: str) -> int:
    return {
        "single_page_answerable": 85,
        "needs_more_sources": 45,
        "too_broad": 35,
        "too_risky": 10,
        "too_visual": 25,
    }.get(label, 0)


def classify_topic_lifecycle(
    answer_status: AnswerStatus,
    heat_score: int,
    growth_score: int,
    freshness_score: int,
    evidence_quality: int,
    evergreen_value: int,
) -> Literal["new", "rising", "stable", "declining", "resolved", "stale"]:
    if answer_status == AnswerStatus.answered and evidence_quality >= 65:
        return "resolved"
    if freshness_score >= 85 and evidence_quality < 45:
        return "new"
    if (growth_score >= 70 or freshness_score >= 75) and answer_status in {AnswerStatus.unanswered, AnswerStatus.partial}:
        return "rising"
    if freshness_score <= 20 and heat_score < 45:
        return "stale"
    if freshness_score <= 30 and growth_score <= 10:
        return "declining"
    if evergreen_value >= 60 or evidence_quality >= 55:
        return "stable"
    return "new"


def classify_topic_actionability(
    need_key: str,
    answer_status: AnswerStatus,
    risk_level: str,
    evidence_quality: int,
) -> tuple[Literal["single_page_answerable", "needs_more_sources", "too_broad", "too_risky", "too_visual"], list[str]]:
    if risk_level == "high":
        return "too_risky", ["High-risk advice should not enter normal article generation."]
    if need_key == "map_exploration_route":
        return "too_visual", ["Map-heavy topics need careful treatment without copying maps or images."]
    if need_key == "build_loadout":
        return "too_broad", ["Build/loadout topics can be broad and need tighter scoping before drafting."]
    if answer_status in {AnswerStatus.unanswered, AnswerStatus.unknown} or evidence_quality < 45:
        return "needs_more_sources", ["More credible sources are needed before a useful page can be written."]
    return "single_page_answerable", ["The topic can likely become one focused source-backed Piko page."]


def classify_competition_gap(score: int, coverage_level: str = "partial", freshness_score: int = 0) -> Literal["strong", "weak", "fragmented", "stale", "absent"]:
    if score >= 90:
        return "absent"
    if score >= 70:
        return "fragmented"
    if freshness_score <= 20 and score >= 55:
        return "stale"
    if score >= 45 or coverage_level == "partial":
        return "weak"
    return "strong"


def content_opportunity_score_for(
    decision: DiscoveryDecision,
    heat_score: int,
    answer_status: AnswerStatus,
    evidence_quality: int,
    risk_level: str,
    actionability_score: int,
    competition_gap: int,
    piko_value_add_score: int,
) -> tuple[int, list[str]]:
    score = round(
        0.22 * heat_score
        + 0.18 * evidence_quality
        + 0.2 * actionability_score
        + 0.2 * competition_gap
        + 0.2 * piko_value_add_score
    )
    reasons = [
        f"Topic heat contributes {heat_score}.",
        f"Evidence maturity contributes {evidence_quality}.",
        f"Actionability contributes {actionability_score}.",
        f"Competition gap contributes {competition_gap}.",
        f"Piko value add contributes {piko_value_add_score}.",
    ]
    if answer_status == AnswerStatus.answered:
        score += 6
        reasons.append("Credible answer maturity improves content opportunity.")
    if decision == DiscoveryDecision.publish_candidate:
        score += 8
        reasons.append("Publish-candidate routing improves content creation priority.")
    if decision == DiscoveryDecision.conflict_explainer:
        score -= 4
        reasons.append("Conflicting answers require synthesis rather than a normal solution page.")
    if decision == DiscoveryDecision.watchlist_waiting_for_answer:
        score -= 35
        reasons.append("Watchlist topics should wait for answer maturity before content creation.")
    if risk_level == "high" or decision == DiscoveryDecision.blocked_high_risk:
        score -= 55
        reasons.append("High-risk topics are blocked from normal content creation priority.")
    return clamp_score(score), reasons
