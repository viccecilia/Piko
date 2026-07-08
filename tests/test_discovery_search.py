import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from packages.discovery.fixtures import load_discovery_fixtures
from packages.discovery.funnel_trace import discovery_funnel_trace
from packages.discovery.improvement_signals import improvement_signals_from_discovery
from packages.discovery.real_source import (
    DiscoveryRealSourceConfigurationError,
    DiscoveryLiveSmokeSkipped,
    DiscoveryRealSourceDisabledError,
    FixtureDiscoverySource,
    RealDiscoveryEndpoint,
    RealMarketDiscoverySource,
    discovery_live_smoke_contract,
    run_discovery_live_smoke,
)
from packages.discovery.real_market_live_smoke import (
    real_market_live_smoke_contract,
    run_real_market_live_smoke,
)
from packages.discovery.real_market_pilot import real_market_candidate_pilot
from packages.discovery.real_endpoint_contract import (
    approved_endpoint_contract,
    load_approved_endpoint_fixture,
    normalize_approved_endpoint_payload,
    validate_approved_endpoint_payload,
)
from packages.discovery.real_endpoint_verify import (
    verify_fixture,
    verify_live,
    verify_mock_live_payload,
    write_endpoint_verification_artifact,
)
from packages.discovery.rev_pipeline import (
    LATEST_ARTICLE_PACKAGE_PATH,
    LATEST_FUNNEL_REPORT_PATH,
    LATEST_PUBLISH_READINESS_PATH,
    approved_live_source_registry,
    build_latest_real_market_funnel_report,
    endpoint_fed_rankings,
    operator_result_surface,
    run_real_search_endpoint_adapter,
    selected_safe_topic_candidate,
    source_hints_and_evidence_readiness,
    write_latest_real_market_funnel_report,
    write_publish_readiness_metadata,
    write_source_backed_article_package,
)
from packages.discovery.real_market import (
    REAL_MARKET_SOURCE_CATEGORIES,
    RealMarketConfigError,
    bounded_real_market_limits,
    normalize_real_market_payloads,
    real_market_policy,
    real_market_source_contract,
    validate_real_market_collection_config,
)
from packages.discovery.scoring import (
    DISCOVERY_SCORE_INPUTS,
    answer_status_for,
    classify_competition_gap,
    classify_topic_actionability,
    classify_topic_lifecycle,
    content_opportunity_score_for,
    decision_for,
    question_heat_score,
    score_game_heat,
)
from packages.discovery.rankings import hot_strategy_rankings, rank_hot_games
from apps.api.main import app
from packages.collectors.real_market import (
    JPCommunityMarketConnector,
    KRCommunityMarketConnector,
    RedditMarketConnector,
    SERPMarketConnector,
    SteamMarketConnector,
)
from packages.discovery.search_engine import (
    article_candidate_from_cluster,
    discovery_retrospective_report,
    normalization_hints_for_question,
    PLANNED_TOPIC_SOURCE_TYPES,
    piko_value_add_for_decision,
    promotion_candidate_from_watchlist,
    region_signal_score_for,
    region_signal_summary_for,
    search_intent_for_need_key,
    select_publish_article_candidates,
    search_player_needs,
    source_coverage_for,
    watchlist_refresh_plan_for,
    watchlist_state_for_signal,
    watchlist_items_from_clusters,
)
from packages.improvement.upgrade_ledger import append_ledger_entry
from packages.improvement.patch_plan import patch_plan_from_proposal
from packages.improvement.proposal_agent import proposal_from_diagnostic
from packages.shared.config import get_settings
from packages.shared.schemas import (
    AnswerStatus,
    ArticleWorkflowRequest,
    DiscoveryArticleCandidate,
    DiagnosticReport,
    DiscoveryDecision,
    DiscoverySearchRequest,
    GameHeatSignal,
    PlayerQuestionSignal,
)
from packages.workflows.candidate_pipeline import (
    candidate_to_article_workflow_request,
    run_candidate_article_workflow,
    write_candidate_workflow_artifacts,
)


client = TestClient(app)


def test_discovery_search_returns_funnel_decisions() -> None:
    result = search_player_needs(DiscoverySearchRequest(min_game_heat=50))
    decisions = {cluster.decision for cluster in result.clusters}

    assert result.real_collection_performed is False
    assert DiscoveryDecision.publish_candidate in decisions
    assert DiscoveryDecision.watchlist_waiting_for_answer in decisions
    assert DiscoveryDecision.conflict_explainer in decisions
    assert DiscoveryDecision.blocked_high_risk in decisions
    assert result.funnel_counts["publish_candidate"] >= 1
    assert DISCOVERY_SCORE_INPUTS == [
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


def test_publish_candidate_has_answer_and_value_add() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(
            query="stardew save",
            decisions=[DiscoveryDecision.publish_candidate],
        )
    )

    assert result.clusters
    cluster = result.clusters[0]
    assert cluster.game_name == "Stardew Valley"
    assert cluster.answer_status == "answered"
    assert cluster.evidence_quality >= 60
    assert cluster.score_inputs["game_heat"] >= 0
    assert cluster.score_inputs["question_heat"] == cluster.heat_score
    assert cluster.score_inputs["evidence_quality"] == cluster.evidence_quality
    assert cluster.score_inputs["competition_gap"] == cluster.competition_gap
    assert cluster.competition_gap_status == "fragmented"
    assert cluster.score_inputs["actionability_score"] == cluster.actionability_score
    assert cluster.score_inputs["piko_value_add_score"] == cluster.piko_value_add_score
    assert cluster.content_opportunity_score >= 70
    assert cluster.score_inputs["content_opportunity_score"] == cluster.content_opportunity_score
    assert cluster.topic_lifecycle == "resolved"
    assert cluster.actionability_label == "single_page_answerable"
    assert "source-traced guide" in " ".join(cluster.piko_value_add)


def test_topic_score_components_are_visible_and_explainable() -> None:
    result = search_player_needs(DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate]))
    cluster = result.clusters[0]

    assert set(cluster.topic_score_components) == {
        "topic_heat",
        "urgency",
        "evidence_maturity",
        "conflict_level",
        "risk_level",
        "freshness",
        "evergreen_value",
        "competition_gap",
        "actionability",
        "piko_value_add",
        "content_opportunity",
    }
    assert cluster.topic_score_components["topic_heat"] == cluster.heat_score
    assert cluster.topic_score_components["actionability"] == cluster.actionability_score
    assert cluster.topic_score_components["content_opportunity"] == cluster.content_opportunity_score
    assert cluster.reasons
    assert cluster.actionability_reasons


def test_competition_gap_contract_distinguishes_gap_from_evidence_quality() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )
    cluster = result.clusters[0]

    assert cluster.answer_status == AnswerStatus.answered
    assert cluster.evidence_quality >= 70
    assert cluster.competition_gap >= 70
    assert cluster.competition_gap_status == "fragmented"
    assert any("Competition gap status: fragmented" in reason for reason in cluster.reasons)
    assert classify_competition_gap(95) == "absent"
    assert classify_competition_gap(75) == "fragmented"
    assert classify_competition_gap(60, freshness_score=10) == "stale"
    assert classify_competition_gap(20, coverage_level="broad") == "strong"


def test_content_opportunity_ranking_prefers_publish_over_watchlist_and_high_risk() -> None:
    result = search_player_needs(DiscoverySearchRequest(limit=20))
    by_decision = {cluster.decision: cluster for cluster in result.clusters}

    publish = by_decision[DiscoveryDecision.publish_candidate]
    watchlist = by_decision[DiscoveryDecision.watchlist_waiting_for_answer]
    high_risk = by_decision[DiscoveryDecision.blocked_high_risk]

    assert result.clusters[0].decision == DiscoveryDecision.publish_candidate
    assert publish.content_opportunity_score > watchlist.content_opportunity_score
    assert publish.content_opportunity_score > high_risk.content_opportunity_score
    assert high_risk.content_opportunity_score < 50
    assert any("High-risk topics are blocked" in reason for reason in high_risk.content_opportunity_reasons)

    score, reasons = content_opportunity_score_for(
        DiscoveryDecision.publish_candidate,
        heat_score=75,
        answer_status=AnswerStatus.answered,
        evidence_quality=80,
        risk_level="low",
        actionability_score=85,
        competition_gap=80,
        piko_value_add_score=80,
    )
    assert score >= 80
    assert any("Credible answer maturity" in reason for reason in reasons)


def test_piko_value_add_reasons_cover_non_ignore_decisions() -> None:
    expected_phrase = {
        DiscoveryDecision.publish_candidate: "Single-page clarity",
        DiscoveryDecision.watchlist_waiting_for_answer: "Monitoring value",
        DiscoveryDecision.conflict_explainer: "Conflict explanation",
        DiscoveryDecision.evergreen_candidate: "Evergreen utility",
        DiscoveryDecision.rising_opportunity: "Freshness value",
        DiscoveryDecision.blocked_high_risk: "Risk warning",
    }

    for decision, phrase in expected_phrase.items():
        reasons = piko_value_add_for_decision(
            decision,
            cross_language=True,
            competition_gap_status="fragmented",
            actionability_label="single_page_answerable",
        )
        assert reasons
        assert any(phrase in reason for reason in reasons)
        assert any("Cross-language bridge" in reason for reason in reasons)
        assert any("Gap fill" in reason for reason in reasons)

    result = search_player_needs(DiscoverySearchRequest(limit=20))
    non_ignore = [cluster for cluster in result.clusters if cluster.decision != DiscoveryDecision.ignore]
    assert non_ignore
    assert all(cluster.piko_value_add for cluster in non_ignore)


def test_unanswered_hot_issue_goes_to_watchlist() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(
            query="hades crash",
            decisions=[DiscoveryDecision.watchlist_waiting_for_answer],
        )
    )

    assert result.clusters
    cluster = result.clusters[0]
    assert cluster.answer_status == "unanswered"
    assert cluster.monitor_reason
    assert "Monitor" in cluster.recommended_article_intent


def test_high_risk_issue_is_blocked() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(
            query="recovery tool",
            decisions=[DiscoveryDecision.blocked_high_risk],
        )
    )

    assert result.clusters
    cluster = result.clusters[0]
    assert cluster.risk_level == "high"
    assert cluster.decision == DiscoveryDecision.blocked_high_risk
    assert cluster.score_inputs["risk_level"] == "high"


def test_discovery_score_boundaries_are_clamped() -> None:
    cold_game = score_game_heat(
        GameHeatSignal(
            game_id="cold",
            game_name="Cold Game",
            steam_player_rank=999,
            steam_review_velocity=-50,
            community_post_velocity=-30,
            update_recency_days=999,
            cross_region_mentions=0,
        )
    )
    hot_game = score_game_heat(
        GameHeatSignal(
            game_id="hot",
            game_name="Hot Game",
            steam_player_rank=1,
            steam_review_velocity=999,
            community_post_velocity=999,
            update_recency_days=0,
            cross_region_mentions=99,
        )
    )
    hot_question = PlayerQuestionSignal(
        question_id="q_hot",
        game_id="hot",
        game_name="Hot Game",
        question_text="Where is the save file?",
        source_type="fixture",
        engagement_count=9999,
        reply_count=999,
        duplicate_count=999,
        growth_24h=999,
    )

    assert cold_game.heat_score == 0
    assert 0 <= hot_game.heat_score <= 100
    assert question_heat_score(hot_question, 999) == 100


def test_discovery_decision_contract_matrix() -> None:
    assert (
        decision_for(
            AnswerStatus.answered,
            heat_score=90,
            evidence_quality=90,
            risk_level="high",
            growth_score=0,
            evergreen=False,
            cross_language=False,
        )
        == DiscoveryDecision.blocked_high_risk
    )
    assert (
        decision_for(
            AnswerStatus.conflicting,
            heat_score=70,
            evidence_quality=70,
            risk_level="low",
            growth_score=0,
            evergreen=False,
            cross_language=False,
        )
        == DiscoveryDecision.conflict_explainer
    )
    assert (
        decision_for(
            AnswerStatus.unanswered,
            heat_score=70,
            evidence_quality=50,
            risk_level="low",
            growth_score=0,
            evergreen=False,
            cross_language=False,
        )
        == DiscoveryDecision.watchlist_waiting_for_answer
    )
    assert (
        decision_for(
            AnswerStatus.answered,
            heat_score=70,
            evidence_quality=70,
            risk_level="low",
            growth_score=0,
            evergreen=False,
            cross_language=False,
            piko_value_add_score=70,
        )
        == DiscoveryDecision.publish_candidate
    )
    assert (
        decision_for(
            AnswerStatus.partial,
            heat_score=58,
            evidence_quality=50,
            risk_level="low",
            growth_score=40,
            evergreen=False,
            cross_language=False,
            freshness_score=80,
        )
        == DiscoveryDecision.rising_opportunity
    )
    assert (
        decision_for(
            AnswerStatus.partial,
            heat_score=40,
            evidence_quality=60,
            risk_level="low",
            growth_score=0,
            evergreen=True,
            cross_language=False,
        )
        == DiscoveryDecision.evergreen_candidate
    )
    assert (
        decision_for(
            AnswerStatus.partial,
            heat_score=40,
            evidence_quality=30,
            risk_level="low",
            growth_score=0,
            evergreen=False,
            cross_language=False,
        )
        == DiscoveryDecision.insufficient_evidence
    )


def test_topic_lifecycle_classifier_examples() -> None:
    assert classify_topic_lifecycle(AnswerStatus.unanswered, 80, 85, 90, 20, 30) == "new"
    assert classify_topic_lifecycle(AnswerStatus.partial, 70, 80, 75, 50, 30) == "rising"
    assert classify_topic_lifecycle(AnswerStatus.partial, 55, 5, 35, 60, 80) == "stable"
    assert classify_topic_lifecycle(AnswerStatus.partial, 35, 0, 10, 50, 20) == "stale"
    assert classify_topic_lifecycle(AnswerStatus.answered, 60, 0, 30, 80, 85) == "resolved"


def test_topic_actionability_classifier_examples() -> None:
    assert classify_topic_actionability("save_file_location", AnswerStatus.answered, "low", 75)[0] == "single_page_answerable"
    assert classify_topic_actionability("crash_after_update", AnswerStatus.unanswered, "medium", 30)[0] == "needs_more_sources"
    assert classify_topic_actionability("build_loadout", AnswerStatus.answered, "low", 65)[0] == "too_broad"
    assert classify_topic_actionability("save_recovery_risk", AnswerStatus.conflicting, "high", 20)[0] == "too_risky"
    assert classify_topic_actionability("map_exploration_route", AnswerStatus.partial, "low", 55)[0] == "too_visual"


def test_discovery_api_search_is_offline_fixture_mode() -> None:
    response = client.post("/discovery/search", json={"query": "stardew", "limit": 5})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["mode"] == "fixture"
    assert payload["real_collection_performed"] is False
    assert payload["clusters"]


def test_every_discovery_decision_has_targeted_coverage() -> None:
    decisions = {
        decision_for(AnswerStatus.answered, 70, 70, "low", 0, False, False, piko_value_add_score=70),
        decision_for(AnswerStatus.unanswered, 70, 30, "low", 0, False, False),
        decision_for(AnswerStatus.conflicting, 70, 60, "low", 0, False, False),
        decision_for(AnswerStatus.partial, 30, 60, "low", 0, True, False),
        decision_for(AnswerStatus.partial, 70, 50, "low", 80, False, False),
        decision_for(AnswerStatus.answered, 90, 90, "high", 0, False, False),
        decision_for(AnswerStatus.partial, 30, 30, "low", 0, False, False),
        decision_for(AnswerStatus.partial, 30, 50, "low", 0, False, False),
    }

    assert decisions == set(DiscoveryDecision)


def test_fixture_loader_covers_common_player_need_types_and_short_snippets() -> None:
    _, questions = load_discovery_fixtures()
    tags = {tag for question in questions for tag in question.tags}
    source_types = {question.source_type for question in questions}

    assert {"crash", "save", "settings", "build", "map", "quest", "hidden"}.issubset(tags)
    assert {"steam_discussion", "reddit", "wiki_comment", "official_forum", "serp_snippet"}.issubset(source_types)
    assert all(question.snippet is None or len(question.snippet) <= 500 for question in questions)
    assert all("raw_text" not in question.metadata for question in questions)


def test_need_key_classifier_and_multilingual_dedup_preserve_regions() -> None:
    result = search_player_needs(DiscoverySearchRequest(limit=20))
    by_key = {cluster.need_key: cluster for cluster in result.clusters}

    assert {"save_file_location", "settings_steam_deck", "build_loadout", "map_exploration_route", "quest_route", "hidden_item"}.issubset(by_key)
    save_cluster = by_key["save_file_location"]
    assert {"en", "jp"}.issubset(set(save_cluster.source_regions))
    assert len(save_cluster.representative_questions) >= 2
    assert save_cluster.source_diversity_count >= 3
    assert save_cluster.duplicate_count >= 1
    assert save_cluster.representative_question_id == "q_stardew_save_steam_001"
    assert "save" in save_cluster.normalization_hints
    assert "location" in save_cluster.normalization_hints


def test_search_intent_taxonomy_maps_representative_needs() -> None:
    assert search_intent_for_need_key("crash_after_update") == "bug_fix"
    assert search_intent_for_need_key("controller_input_issue") == "bug_fix"
    assert search_intent_for_need_key("save_file_location") == "save_file"
    assert search_intent_for_need_key("settings_steam_deck") == "settings"
    assert search_intent_for_need_key("build_loadout") == "build"
    assert search_intent_for_need_key("map_exploration_route") == "map_exploration"
    assert search_intent_for_need_key("hidden_item") == "hidden_item"
    assert search_intent_for_need_key("quest_route") == "quest_blocker"

    result = search_player_needs(DiscoverySearchRequest(limit=20))
    by_key = {cluster.need_key: cluster for cluster in result.clusters}
    assert by_key["crash_after_update"].search_intent == "bug_fix"
    assert by_key["save_file_location"].search_intent == "save_file"
    assert by_key["settings_steam_deck"].search_intent == "settings"
    assert by_key["build_loadout"].search_intent == "build"
    assert by_key["map_exploration_route"].search_intent == "map_exploration"
    assert by_key["hidden_item"].search_intent == "hidden_item"
    assert by_key["quest_route"].search_intent == "quest_blocker"


def test_repeated_questions_cluster_without_dropping_minority_language_examples() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(
            query="stardew save",
            decisions=[DiscoveryDecision.publish_candidate],
            limit=20,
        )
    )
    assert len(result.clusters) == 1
    cluster = result.clusters[0]

    assert cluster.need_key == "save_file_location"
    assert cluster.search_intent == "save_file"
    assert cluster.representative_question_id == "q_stardew_save_steam_001"
    assert "jp" in cluster.source_regions
    assert any(question != cluster.representative_question for question in cluster.representative_questions)
    assert cluster.duplicate_count == 13


def test_multilingual_normalization_hints_classify_jp_and_kr_terms() -> None:
    jp_hints = normalization_hints_for_question("セーブデータの場所はどこですか", [])
    kr_hints = normalization_hints_for_question("저장 위치 오류가 있나요", [])
    map_hints = normalization_hints_for_question("지도 루트가 어디인가요", [])

    assert {"save", "location"}.issubset(jp_hints)
    assert {"save", "location", "bug"}.issubset(kr_hints)
    assert {"map", "location"}.issubset(map_hints)


def test_region_signal_model_marks_cross_region_language_gap() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )
    cluster = result.clusters[0]

    assert cluster.cross_region_repeat is True
    assert cluster.language_gap_opportunity is True
    assert cluster.region_signal_score > 0
    assert cluster.region_signal_summary["regions"] == ["en", "jp"]
    assert cluster.region_signal_summary["duplicate_count_by_region"]["en"] == 8
    assert cluster.region_signal_summary["duplicate_count_by_region"]["jp"] == 5
    assert any("Language-gap opportunity" in reason for reason in cluster.reasons)
    assert any("Cross-language bridge" in value for value in cluster.piko_value_add)


def test_region_signal_helpers_do_not_require_real_collection() -> None:
    questions = [
        PlayerQuestionSignal(
            question_id="q_en",
            game_id="game",
            game_name="Game",
            question_text="Where is the save file?",
            source_type="steam_discussion",
            source_region="en",
            duplicate_count=3,
        ),
        PlayerQuestionSignal(
            question_id="q_kr",
            game_id="game",
            game_name="Game",
            question_text="저장 위치가 어디인가요",
            source_type="wiki_comment",
            source_region="kr",
            duplicate_count=2,
        ),
    ]
    summary = region_signal_summary_for(questions)

    assert summary["cross_region_repeat"] is True
    assert summary["language_gap_opportunity"] is True
    assert region_signal_score_for(summary) > 0


def test_source_coverage_matrix_is_visible_and_honest_about_gaps() -> None:
    result = search_player_needs(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )
    cluster = result.clusters[0]

    assert cluster.source_coverage["current_source_types"] == ["steam_discussion", "wiki_comment"]
    assert cluster.source_coverage["planned_source_types"] == PLANNED_TOPIC_SOURCE_TYPES
    assert cluster.source_coverage["source_type_diversity_count"] == 2
    assert cluster.source_coverage["source_region_diversity_count"] == 2
    assert "reddit" in cluster.source_coverage["missing_source_types"]
    assert "kr" in cluster.source_coverage["regional_gaps"]
    assert cluster.source_coverage["coverage_level"] == "partial"
    assert cluster.source_coverage["real_collection_performed"] is False

    thin = source_coverage_for(["serp_snippet"], ["en"])
    assert thin["coverage_level"] == "thin"


def test_answer_state_classifier_covers_all_states() -> None:
    base = {
        "question_id": "q",
        "game_id": "g",
        "game_name": "Game",
        "question_text": "Question?",
        "source_type": "fixture",
    }

    assert answer_status_for([]) == AnswerStatus.unknown
    assert answer_status_for([PlayerQuestionSignal(**base)]) == AnswerStatus.unanswered
    assert answer_status_for([PlayerQuestionSignal(**base, evidence_quality=50)]) == AnswerStatus.partial
    assert answer_status_for([PlayerQuestionSignal(**base, has_accepted_answer=True)]) == AnswerStatus.answered
    assert answer_status_for([PlayerQuestionSignal(**base, answer_conflict_count=1, has_accepted_answer=True)]) == AnswerStatus.conflicting


def test_evidence_maturity_and_risk_conflict_routing_boundaries() -> None:
    assert decision_for(AnswerStatus.answered, 70, 59, "low", 0, False, False) != DiscoveryDecision.publish_candidate
    assert decision_for(AnswerStatus.answered, 70, 60, "low", 0, False, False) == DiscoveryDecision.publish_candidate
    assert decision_for(AnswerStatus.answered, 90, 90, "high", 0, False, False) == DiscoveryDecision.blocked_high_risk
    assert decision_for(AnswerStatus.conflicting, 55, 50, "low", 0, False, False) == DiscoveryDecision.conflict_explainer


def test_watchlist_items_and_promotion_signal_are_candidate_only() -> None:
    result = search_player_needs(DiscoverySearchRequest(decisions=[DiscoveryDecision.watchlist_waiting_for_answer]))
    watchlist = watchlist_items_from_clusters(result.clusters)
    assert watchlist
    item = watchlist[0]
    assert item.state == "watching"
    assert item.publish_ready is False
    assert item.requires_evidence_pipeline is True
    assert "accepted_answer" in item.trigger_conditions
    assert "evidence_ready" in item.state_transitions
    assert item.refresh_interval_hours == 6
    assert "High-growth" in item.next_check_reason

    signal = PlayerQuestionSignal(
        question_id="q_new_answer",
        game_id="hades_ii",
        game_name="Hades II",
        question_text="A fix was accepted.",
        source_type="steam_discussion",
        has_accepted_answer=True,
        evidence_quality=70,
    )
    promoted = promotion_candidate_from_watchlist(item, signal)
    assert promoted["previous_state"] == "watching"
    assert promoted["next_state"] == "evidence_ready"
    assert promoted["recommended_next_action"] == "send_to_evidence_pipeline"
    assert promoted["publish_ready"] is False
    assert promoted["publishing_performed"] is False


def test_watchlist_state_machine_transitions_are_explicit() -> None:
    base = {
        "question_id": "q",
        "game_id": "hades_ii",
        "game_name": "Hades II",
        "question_text": "Hades II crashes after the latest patch, is there a fix?",
        "source_type": "steam_discussion",
    }

    assert watchlist_state_for_signal(PlayerQuestionSignal(**base), freshness_score=90, heat_score=90) == "watching"
    assert (
        watchlist_state_for_signal(
            PlayerQuestionSignal(**base, has_accepted_answer=True, evidence_quality=45),
            freshness_score=90,
            heat_score=90,
        )
        == "answer_seen"
    )
    assert (
        watchlist_state_for_signal(
            PlayerQuestionSignal(**base, has_official_answer=True, evidence_quality=70),
            freshness_score=90,
            heat_score=90,
        )
        == "evidence_ready"
    )
    assert watchlist_state_for_signal(PlayerQuestionSignal(**base), freshness_score=10, heat_score=30) == "stale"


def test_watchlist_refresh_plan_shortens_for_high_growth_unresolved_topics() -> None:
    hot = search_player_needs(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.watchlist_waiting_for_answer])
    ).clusters[0]
    interval, reason = watchlist_refresh_plan_for(hot)

    assert interval == 6
    assert "High-growth" in reason

    stale_cluster = hot.model_copy(update={"topic_lifecycle": "stale", "freshness_score": 10, "urgency_score": 5})
    stale_interval, stale_reason = watchlist_refresh_plan_for(stale_cluster)

    assert stale_interval == 72
    assert "Low-freshness" in stale_reason


def test_article_candidate_handoff_includes_hints_and_safety_gate() -> None:
    result = search_player_needs(DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate]))
    candidate = article_candidate_from_cluster(result.clusters[0])

    assert candidate.game_id == "stardew_valley"
    assert candidate.game_name == "Stardew Valley"
    assert candidate.cluster_id == result.clusters[0].cluster_id
    assert candidate.decision == DiscoveryDecision.publish_candidate
    assert candidate.need_key == "save_file_location"
    assert candidate.player_question
    assert candidate.article_intent
    assert candidate.source_search_hints
    assert candidate.source_query_hints == candidate.source_search_hints
    assert candidate.risk_level == "low"
    assert candidate.risk_flags == []
    assert candidate.runnable is True
    assert candidate.candidate_type == "solution_candidate"
    assert candidate.publish_ready is False
    assert candidate.requires_evidence_pipeline is True

    round_trip = DiscoveryArticleCandidate.model_validate_json(candidate.model_dump_json())
    assert round_trip == candidate

    blocked = search_player_needs(DiscoverySearchRequest(decisions=[DiscoveryDecision.blocked_high_risk])).clusters[0]
    blocked_candidate = article_candidate_from_cluster(blocked)
    assert blocked_candidate.publish_ready is False
    assert blocked_candidate.runnable is False
    assert blocked_candidate.candidate_type == "blocked_safety_note"
    assert "high_risk_block" in blocked_candidate.safety_flags
    assert any("High-risk" in note for note in blocked_candidate.safety_notes)


def test_candidate_safety_contract_blocks_watchlist_and_high_risk() -> None:
    watchlist_cluster = search_player_needs(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.watchlist_waiting_for_answer])
    ).clusters[0]
    watchlist_candidate = article_candidate_from_cluster(watchlist_cluster)

    assert watchlist_candidate.publish_ready is False
    assert watchlist_candidate.requires_evidence_pipeline is True
    assert watchlist_candidate.runnable is False
    assert watchlist_candidate.candidate_type == "watchlist_only"
    assert "watchlist_only" in watchlist_candidate.safety_flags
    assert "no_credible_answer_yet" in watchlist_candidate.risk_flags

    high_risk_cluster = search_player_needs(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.blocked_high_risk])
    ).clusters[0]
    high_risk_candidate = article_candidate_from_cluster(high_risk_cluster)

    assert high_risk_candidate.publish_ready is False
    assert high_risk_candidate.runnable is False
    assert high_risk_candidate.candidate_type == "blocked_safety_note"
    assert "high_risk_block" in high_risk_candidate.safety_flags
    assert "risk_level:high" in high_risk_candidate.risk_flags


def test_conflict_candidate_is_synthesis_not_normal_solution() -> None:
    conflict_cluster = search_player_needs(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.conflict_explainer])
    ).clusters[0]
    candidate = article_candidate_from_cluster(conflict_cluster)

    assert candidate.publish_ready is False
    assert candidate.requires_evidence_pipeline is True
    assert candidate.runnable is True
    assert candidate.candidate_type == "synthesis_candidate"
    assert "synthesis_only" in candidate.safety_flags
    assert "conflicting_answers" in candidate.risk_flags
    assert any("uncertainty" in reason for reason in candidate.safety_reasons)


def test_select_publish_article_candidates_keeps_only_runnable_publish_candidates() -> None:
    candidates = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )

    assert candidates
    candidate = candidates[0]
    assert candidate.game_name == "Stardew Valley"
    assert candidate.need_key == "save_file_location"
    assert candidate.decision == DiscoveryDecision.publish_candidate
    assert candidate.runnable is True
    assert candidate.publish_ready is False
    assert candidate.requires_evidence_pipeline is True
    assert candidate.piko_value_add
    assert candidate.cluster_reasons
    assert candidate.score_inputs["answer_status"] == "answered"

    watchlist = select_publish_article_candidates(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.watchlist_waiting_for_answer])
    )
    high_risk = select_publish_article_candidates(
        DiscoverySearchRequest(decisions=[DiscoveryDecision.blocked_high_risk])
    )

    assert watchlist == []
    assert high_risk == []


def test_article_candidate_source_query_hints_include_need_and_source_types() -> None:
    candidates = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )
    candidate = candidates[0]
    hint_text = " ".join(candidate.source_query_hints).lower()

    assert "stardew valley" in hint_text
    assert "save file location" in hint_text
    assert any(source_type in hint_text for source_type in candidate.preferred_source_types)
    assert candidate.required_source_types == candidate.preferred_source_types
    assert "wiki_comment" in candidate.preferred_source_types


def test_article_candidate_maps_to_workflow_request_without_publishing() -> None:
    candidate = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )[0]
    request = candidate_to_article_workflow_request(candidate)

    assert isinstance(request, ArticleWorkflowRequest)
    assert request.game_name == "Stardew Valley"
    assert request.game_id == "stardew_valley"
    assert request.player_question == candidate.player_question
    assert request.article_intent == candidate.article_intent
    assert request.candidate_id == candidate.candidate_id
    assert request.cluster_id == candidate.cluster_id
    assert request.source_query_hints == candidate.source_query_hints
    assert request.safety_metadata["candidate_only"] is True
    assert request.safety_metadata["requires_evidence_pipeline"] is True
    assert request.publish_ready is False
    assert request.publishing_performed is False
    assert request.real_collection_performed is False


def test_candidate_workflow_runner_is_fixture_safe_and_non_publishing() -> None:
    candidate = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )[0]
    result = run_candidate_article_workflow(candidate)

    assert result.workflow_request.game_name == "Stardew Valley"
    assert result.workflow_result.status == "completed"
    assert result.workflow_result.pipeline_state.game.game_name == "Stardew Valley"
    assert result.workflow_result.pipeline_state.player_question == candidate.player_question
    assert result.workflow_result.verification_report is not None
    assert result.verification_report is not None
    assert result.verification_report.status in {"pass", "fail", "warning"}
    assert result.publish_action in {"draft_review", "store_only", "discard", "auto_publish_disabled"}
    assert result.publish_ready is False
    assert result.publishing_performed is False
    assert result.real_collection_performed is False
    assert result.candidate_only is True
    assert result.safety_fields["discovery_is_publish_permission"] is False
    assert result.safety_fields["publish_ready"] is False
    assert result.safety_fields["publishing_performed"] is False
    assert result.safety_fields["real_collection_performed"] is False
    if result.verification_report.status != "pass":
        assert result.publish_decision is not None
        assert result.publish_decision.blocks_publish is True
        assert result.publish_decision.value == "verification_failed"


def test_candidate_workflow_result_keeps_verification_and_safety_decisions() -> None:
    candidate = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )[0]
    result = run_candidate_article_workflow(candidate)

    assert result.verification_report is not None
    assert result.verification_report.summary
    assert result.publish_decision is not None
    assert result.publish_decision.value in {
        "verified_candidate",
        "needs_more_evidence",
        "verification_failed",
        "draft_review",
        "do_not_publish",
    }
    assert result.publish_ready is False
    assert result.publishing_performed is False
    assert result.safety_fields["candidate_only"] is True
    assert "candidate_only" in result.safety_fields["safety_flags"]
    assert result.safety_fields["publish_decision_blocks_publish"] is True


def test_candidate_workflow_json_artifact_is_internal_and_non_publishing(tmp_path) -> None:
    candidate = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )[0]
    result = run_candidate_article_workflow(candidate)
    json_path, md_path = write_candidate_workflow_artifacts(candidate, result, directory=str(tmp_path))

    assert json_path.exists()
    assert md_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["artifact_type"] == "discovery_candidate_draft"
    assert payload["status"] == "internal_draft_only"
    assert payload["candidate"]["candidate_id"] == candidate.candidate_id
    assert payload["workflow_request"]["candidate_id"] == candidate.candidate_id
    assert "workflow_result" in payload
    assert "draft" in payload
    assert "sources" in payload
    assert "evidence_cards" in payload
    assert "agent_trace" in payload
    assert "verification_report" in payload
    assert payload["publish_ready"] is False
    assert payload["publishing_performed"] is False
    assert payload["candidate_only"] is True
    assert payload["safety_fields"]["artifact_internal_draft_only"] is True
    assert payload["safety_fields"]["not_public_web_page"] is True
    assert payload["safety_fields"]["long_raw_source_retained"] is False
    assert "raw_text" not in json.dumps(payload, ensure_ascii=False)


def test_candidate_workflow_markdown_artifact_is_readable_internal_draft(tmp_path) -> None:
    candidate = select_publish_article_candidates(
        DiscoverySearchRequest(query="stardew save", decisions=[DiscoveryDecision.publish_candidate])
    )[0]
    result = run_candidate_article_workflow(candidate)
    _, md_path = write_candidate_workflow_artifacts(candidate, result, directory=str(tmp_path))

    markdown = md_path.read_text(encoding="utf-8")
    assert "# Internal Draft:" in markdown
    assert "INTERNAL DRAFT - NOT PUBLISHED" in markdown
    assert "## Safety Status" in markdown
    assert "publish_ready: False" in markdown
    assert "publishing_performed: False" in markdown
    assert "## Evidence Summary" in markdown
    assert "## Sources" in markdown
    assert "## Next Action" in markdown


def test_real_market_topic_candidate_pilot_writes_internal_artifact_and_blocks_unsafe_topics(tmp_path) -> None:
    result = real_market_candidate_pilot(output_dir=str(tmp_path))

    assert result["status"] == "completed"
    assert result["mode"] == "fixture-mock-real-market-equivalent"
    assert result["selected_topic"]["decision"] == "publish_candidate"
    assert result["selected_topic"]["runnable"] is True
    assert result["publish_ready"] is False
    assert result["publishing_performed"] is False
    assert result["candidate_only"] is True
    assert result["safety_fields"]["discovery_is_publish_permission"] is False

    json_path = result["artifact_paths"]["json"]
    markdown_path = result["artifact_paths"]["markdown"]
    assert json_path
    assert markdown_path
    artifact = json.loads(Path(json_path).read_text(encoding="utf-8"))
    assert artifact["status"] == "internal_draft_only"
    assert artifact["publish_ready"] is False
    assert artifact["publishing_performed"] is False
    assert artifact["safety_fields"]["artifact_internal_draft_only"] is True
    assert artifact["verification_report"] is not None

    assert result["blocked_examples"]["watchlist"]["blocked_from_normal_draft"] is True
    assert result["blocked_examples"]["watchlist"]["runnable"] is False
    assert result["blocked_examples"]["high_risk"]["blocked_from_normal_draft"] is True
    assert result["blocked_examples"]["high_risk"]["runnable"] is False
    assert result["blocked_examples"]["high_risk"]["publish_ready"] is False


def test_discovery_api_operator_filters_and_window() -> None:
    response = client.post(
        "/discovery/search",
        json={
            "game_name": "Hades",
            "regions": ["en"],
            "source_types": ["steam_discussion"],
            "answer_statuses": ["unanswered"],
            "decisions": ["watchlist_waiting_for_answer"],
            "min_game_heat": 50,
            "limit": 5,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["clusters"]
    assert all(cluster["decision"] == "watchlist_waiting_for_answer" for cluster in payload["clusters"])

    window = client.get("/discovery/window")
    assert window.status_code == 200
    assert "Piko Discovery Window" in window.text


def test_discovery_api_filters_topic_dimensions_without_generation() -> None:
    response = client.post(
        "/discovery/search",
        json={
            "query": "stardew save",
            "search_intents": ["save_file"],
            "topic_lifecycles": ["resolved"],
            "actionability_labels": ["single_page_answerable"],
            "regions": ["jp"],
            "decisions": ["publish_candidate"],
            "min_content_opportunity_score": 80,
            "limit": 5,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["clusters"]
    assert payload["real_collection_performed"] is False
    cluster = payload["clusters"][0]
    assert cluster["game_name"] == "Stardew Valley"
    assert cluster["search_intent"] == "save_file"
    assert cluster["topic_lifecycle"] == "resolved"
    assert cluster["actionability_label"] == "single_page_answerable"
    assert cluster["content_opportunity_score"] >= 80
    assert cluster["publish_ready"] is False
    assert "draft" not in payload


def test_discovery_cli_topic_filters_keep_json_and_summary_output() -> None:
    json_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "packages.discovery.search_cli",
            "--decision",
            "publish_candidate",
            "--intent",
            "save_file",
            "--lifecycle",
            "resolved",
            "--actionability",
            "single_page_answerable",
            "--min-opportunity",
            "80",
            "--limit",
            "3",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(json_result.stdout)

    assert payload["real_collection_performed"] is False
    assert payload["clusters"]
    assert payload["clusters"][0]["search_intent"] == "save_file"
    assert payload["clusters"][0]["publish_ready"] is False

    summary_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "packages.discovery.search_cli",
            "--decision",
            "watchlist_waiting_for_answer",
            "--intent",
            "bug_fix",
            "--view",
            "summary",
            "--limit",
            "3",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "decision\tintent\tgame\tneed_key\topportunity" in summary_result.stdout
    assert "watchlist_waiting_for_answer\tbug_fix\tHades II\tcrash_after_update" in summary_result.stdout


def test_discovery_report_and_improvement_signals_are_safe(tmp_path) -> None:
    result = search_player_needs(DiscoverySearchRequest(limit=20))
    report = discovery_retrospective_report(result.clusters)
    signals = improvement_signals_from_discovery(result.clusters)

    assert report.status == "completed"
    assert report.decision_counts
    assert report.recommendations
    assert report.real_collection_performed is False
    assert signals
    assert all("raw_text" not in signal.model_dump(mode="json") for signal in signals)

    diagnostic = DiagnosticReport(diagnostic_id="diagnostic_discovery", status="needs_improvement", signals=signals[:1])
    proposal = proposal_from_diagnostic(diagnostic)
    patch_plan = patch_plan_from_proposal(proposal)
    target = tmp_path / "discovery_ledger.jsonl"
    append_ledger_entry({"proposal": proposal.model_dump(mode="json"), "patch_plan": patch_plan.model_dump(mode="json"), "notes": ["safe discovery signal"]}, str(target))
    assert target.exists()


def test_discovery_real_source_interface_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    get_settings.cache_clear()
    try:
        FixtureDiscoverySource().search_questions("Hades II")
    except DiscoveryRealSourceDisabledError as exc:
        assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
    else:
        raise AssertionError("real discovery source should be disabled by default")
    finally:
        get_settings.cache_clear()


def test_topic_discovery_live_smoke_contract_skips_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    get_settings.cache_clear()
    try:
        contract = discovery_live_smoke_contract()
        assert contract["selected_source"] == "pcgamingwiki_mediawiki"
        assert contract["enabled"] is False
        assert contract["max_result_limit"] == 3
        assert contract["real_collection_performed"] is False
        assert "raw full page text" in contract["prohibited_retention"]

        try:
            run_discovery_live_smoke("Stardew Valley")
        except DiscoveryLiveSmokeSkipped as exc:
            assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
        else:
            raise AssertionError("live smoke should skip by default")
    finally:
        get_settings.cache_clear()


def test_topic_discovery_live_smoke_fixture_is_bounded_when_opted_in(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    get_settings.cache_clear()
    try:
        result = run_discovery_live_smoke("Stardew Valley", limit=10)
    finally:
        get_settings.cache_clear()

    assert result["status"] == "completed"
    assert result["selected_source"] == "pcgamingwiki_mediawiki"
    assert result["result_limit"] <= 3
    assert result["real_collection_performed"] is False
    assert result["publishing_performed"] is False
    record = result["records"][0]
    assert record["source_type"] == "pcgamingwiki_mediawiki"
    assert len(record["snippet"]) <= 500
    assert record["metadata"]["raw_text_included"] is False
    assert "raw_text" not in record["metadata"]


def test_real_market_live_smoke_skips_by_default_and_without_endpoints(monkeypatch) -> None:
    for name in [
        "PIKO_ENABLE_DISCOVERY_REAL_SOURCE",
        "PIKO_LIVE_DISCOVERY_TEST",
        "PIKO_STEAM_DISCOVERY_URL",
        "PIKO_REDDIT_DISCOVERY_URL",
        "PIKO_JP_COMMUNITY_DISCOVERY_URL",
        "PIKO_KR_COMMUNITY_DISCOVERY_URL",
        "PIKO_SERP_DISCOVERY_URL",
    ]:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()
    try:
        contract = real_market_live_smoke_contract()
        assert contract["enabled"] is False
        assert contract["real_collection_performed"] is False
        assert contract["publishing_performed"] is False
        try:
            run_real_market_live_smoke("Stardew Valley")
        except DiscoveryLiveSmokeSkipped as exc:
            assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
        else:
            raise AssertionError("real-market live smoke must skip by default")

        monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
        monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
        get_settings.cache_clear()
        contract = real_market_live_smoke_contract()
        assert contract["enabled"] is False
        assert "endpoint" in str(contract["skip_reason"]).lower()
        try:
            run_real_market_live_smoke("Stardew Valley")
        except DiscoveryLiveSmokeSkipped as exc:
            assert "endpoint" in str(exc).lower()
        else:
            raise AssertionError("real-market live smoke must skip without endpoints")
    finally:
        get_settings.cache_clear()


def test_real_market_live_smoke_mock_is_bounded_and_metadata_only(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_STEAM_DISCOVERY_URL", "https://example.invalid/steam")
    get_settings.cache_clear()

    class MockClient:
        def get_json(self, url: str, *, timeout: float, user_agent: str) -> dict[str, object]:
            return {
                "games": [
                    {
                        "app_id": "1145350",
                        "game_name": "Hades II",
                        "rank": 3,
                        "community_post_velocity": 91,
                    }
                ],
                "questions": [
                    {
                        "thread_id": "steam_q_001",
                        "game_name": "Hades II",
                        "title": "Crash after patch?",
                        "snippet": "Short live-smoke summary only.",
                        "body": "must not be retained",
                        "raw_text": "must not be retained",
                        "score": 50,
                        "comment_count": 8,
                    }
                ],
            }

    try:
        result = run_real_market_live_smoke("Hades II", limit_per_source=10, client=MockClient())
    finally:
        get_settings.cache_clear()

    assert result["status"] == "completed"
    assert result["mode"] == "real-source"
    assert result["real_collection_performed"] is True
    assert result["publishing_performed"] is False
    assert result["game_count"] == 1
    assert result["question_count"] == 1
    assert result["full_response_body_saved"] is False
    assert result["contract"]["limits"]["max_records_per_source"] == 3
    serialized = json.dumps(result, ensure_ascii=False)
    assert "must not be retained" not in serialized
    assert "raw_text" not in serialized


def test_real_market_source_contract_lists_categories_and_retention_rules() -> None:
    contract = real_market_source_contract()

    assert contract["source_categories"] == ["steam", "reddit", "jp_community", "kr_community", "serp_snippet"]
    for category in REAL_MARKET_SOURCE_CATEGORIES:
        retained = contract["retained_fields_by_source"][category]
        assert "source_category" in retained
        assert "source_url" in retained
        assert "short_snippet" in retained
        assert "metadata_summary" in retained

    prohibited = set(contract["prohibited_retention"])
    assert {"raw_text", "full posts", "images", "maps", "credentials", "full copied tables"}.issubset(prohibited)
    assert contract["candidate_only"] is True


def test_approved_endpoint_contract_accepts_json_and_rejects_raw_payloads() -> None:
    contract = approved_endpoint_contract()
    payload = load_approved_endpoint_fixture()
    validation = validate_approved_endpoint_payload(payload)

    assert contract["html_pages_approved"] is False
    assert contract["raw_body_endpoints_approved"] is False
    assert {"games", "questions", "source", "generated_at"}.issubset(contract["root_fields"])
    assert validation["status"] == "valid"
    assert validation["game_count"] >= 1
    assert validation["question_count"] >= 4

    unsafe = json.loads(json.dumps(payload))
    unsafe["questions"][0]["raw_text"] = "full copied source must not pass"
    try:
        validate_approved_endpoint_payload(unsafe)
    except RealMarketConfigError as exc:
        assert "prohibited fields" in str(exc)
    else:
        raise AssertionError("raw_text payload should be rejected")

    html_endpoint = json.loads(json.dumps(payload))
    html_endpoint["source"]["endpoint_type"] = "html"
    try:
        validate_approved_endpoint_payload(html_endpoint)
    except RealMarketConfigError as exc:
        assert "JSON endpoints" in str(exc)
    else:
        raise AssertionError("HTML endpoint should be rejected")


def test_approved_endpoint_fixture_mirror_normalizes_and_feeds_rankings() -> None:
    payload = load_approved_endpoint_fixture()
    normalized = normalize_approved_endpoint_payload(payload)
    ranked_games = rank_hot_games(normalized.hot_games, mode="fixture", limit=5)

    assert normalized.real_collection_performed is False
    assert normalized.candidate_only is True
    assert len(normalized.hot_games) >= 1
    assert len(normalized.player_questions) >= 4
    assert ranked_games
    assert ranked_games[0]["mode"] == "fixture"
    source_types = {question.source_type for question in normalized.player_questions}
    assert "steam" in source_types
    assert {"reddit", "serp_snippet", "jp_community"}.intersection(source_types)
    maturity = {question.metadata.get("answer_maturity") for question in normalized.player_questions}
    assert {"answered", "unanswered", "conflicting"}.issubset(maturity)
    assert any(question.risk_level == "high" for question in normalized.player_questions)
    serialized = json.dumps([question.model_dump(mode="json") for question in normalized.player_questions])
    assert "full copied source" not in serialized
    assert "raw_text" not in serialized
    assert "full_comments" not in serialized


def test_real_endpoint_verify_cli_helpers_fixture_and_live_skip(monkeypatch) -> None:
    fixture = verify_fixture()
    assert fixture["status"] == "passed"
    assert fixture["mode"] == "fixture"
    assert fixture["source_count"] == 1
    assert fixture["normalized_game_count"] >= 1
    assert fixture["normalized_question_count"] >= 4
    assert fixture["real_collection_performed"] is False
    assert fixture["publishing_performed"] is False
    assert fixture["safety_flags"]["default_network_disabled"] is True

    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    try:
        skipped = verify_live(None)
        assert skipped["status"] == "skipped"
        assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in skipped["skipped_reason"]

        monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
        monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
        get_settings.cache_clear()
        skipped_no_url = verify_live(None)
        assert skipped_no_url["status"] == "skipped"
        assert "PIKO_APPROVED_ENDPOINT_URL" in skipped_no_url["skipped_reason"]
    finally:
        get_settings.cache_clear()


def test_real_endpoint_mock_live_feeds_rankings_without_claiming_real_collection() -> None:
    payload = load_approved_endpoint_fixture()
    result = verify_mock_live_payload(payload)

    assert result["status"] == "passed"
    assert result["mode"] == "mock-live"
    assert result["real_collection_performed"] is False
    assert result["normalized_game_count"] == 2
    assert result["normalized_question_count"] == 4
    assert result["ranking_preview"]["top_hot_games"]
    assert result["ranking_preview"]["top_hot_games"][0]["mode"] == "mock-live"
    buckets = result["ranking_preview"]["question_buckets"]
    assert buckets["hot_answered_questions"]
    assert buckets["hot_unanswered_watchlist_questions"]
    assert buckets["conflict_answer_topics"]
    assert buckets["high_risk_blocked_topics"]
    assert all(row["publish_ready"] is False for rows in buckets.values() for row in rows)
    assert all(row["runnable"] is False for row in buckets["high_risk_blocked_topics"])


def test_real_endpoint_summary_artifact_is_safe_for_skipped_and_mock_live(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    get_settings.cache_clear()
    try:
        skipped = verify_live(None)
    finally:
        get_settings.cache_clear()
    skipped_path = write_endpoint_verification_artifact(
        skipped,
        directory=tmp_path,
        filename="skipped.json",
    )
    skipped_artifact = json.loads(skipped_path.read_text(encoding="utf-8"))
    assert skipped_artifact["status"] == "skipped"
    assert skipped_artifact["skipped_reason"]
    assert skipped_artifact["raw_response_body_saved"] is False
    assert skipped_artifact["publishing_performed"] is False

    mock_live = verify_mock_live_payload(load_approved_endpoint_fixture())
    mock_path = write_endpoint_verification_artifact(
        mock_live,
        directory=tmp_path,
        filename="mock_live.json",
    )
    artifact_text = mock_path.read_text(encoding="utf-8")
    artifact = json.loads(artifact_text)
    assert artifact["status"] == "passed"
    assert artifact["mode"] == "mock-live"
    assert artifact["normalized_game_count"] == 2
    assert artifact["normalized_question_count"] == 4
    assert artifact["raw_response_body_saved"] is False
    assert artifact["publishing_performed"] is False
    assert "raw_text" not in artifact_text
    assert "authorization" not in artifact_text
    assert "api_key" not in artifact_text


def test_real_market_policy_disabled_by_default_and_missing_endpoints_fail(monkeypatch) -> None:
    for name in [
        "PIKO_ENABLE_DISCOVERY_REAL_SOURCE",
        "PIKO_LIVE_DISCOVERY_TEST",
        "PIKO_STEAM_DISCOVERY_URL",
        "PIKO_REDDIT_DISCOVERY_URL",
        "PIKO_JP_COMMUNITY_DISCOVERY_URL",
        "PIKO_KR_COMMUNITY_DISCOVERY_URL",
        "PIKO_SERP_DISCOVERY_URL",
    ]:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()
    try:
        policy = real_market_policy()
        assert policy["enabled"] is False
        assert policy["default_offline"] is True
        try:
            validate_real_market_collection_config(["steam"])
        except RealMarketConfigError as exc:
            assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
        else:
            raise AssertionError("real-market collection should be disabled by default")

        monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
        monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
        get_settings.cache_clear()
        try:
            validate_real_market_collection_config(["steam", "reddit"])
        except RealMarketConfigError as exc:
            assert "PIKO_STEAM_DISCOVERY_URL" in str(exc)
            assert "PIKO_REDDIT_DISCOVERY_URL" in str(exc)
        else:
            raise AssertionError("missing real-market endpoints should fail clearly")
    finally:
        get_settings.cache_clear()


def test_real_market_limits_are_bounded(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_REAL_MARKET_MAX_SOURCES", "999")
    monkeypatch.setenv("PIKO_REAL_MARKET_MAX_RECORDS_PER_SOURCE", "999")
    get_settings.cache_clear()
    try:
        limits = bounded_real_market_limits()
        assert limits["max_sources"] == 5
        assert limits["max_records_per_source"] == 20
        explicit = bounded_real_market_limits(max_sources=0, max_records_per_source=0)
        assert explicit["max_sources"] == 1
        assert explicit["max_records_per_source"] == 1
    finally:
        get_settings.cache_clear()


def test_real_market_mock_payloads_normalize_without_raw_retention() -> None:
    long_text = "x" * 600
    payloads = {
        "steam": {
            "hot_games": [
                {"app_id": "steam_1", "game_name": "Hot Steam Game", "rank": 7, "velocity": 80, "source_url": "https://steam.example/game"}
            ],
            "player_questions": [
                {
                    "id": "steam_q1",
                    "game_id": "steam_1",
                    "game_name": "Hot Steam Game",
                    "title": "Where is the save file?",
                    "answer_maturity": "answered",
                    "snippet": long_text,
                    "raw_text": "do not keep",
                    "body": "do not keep",
                }
            ],
        },
        "reddit": {
            "hot_games": [{"id": "reddit_1", "title": "Reddit Game", "velocity": 55, "mentions": 4}],
            "player_questions": [
                {
                    "id": "reddit_q1",
                    "game_id": "reddit_1",
                    "game_name": "Reddit Game",
                    "title": "Crash after patch?",
                    "selftext": "full body should be dropped",
                    "answer_maturity": "conflicting",
                    "conflict_count": 2,
                }
            ],
        },
        "jp_community": {
            "hot_games": [{"id": "jp_1", "name": "JP Game", "velocity": 50, "region": "jp"}],
            "player_questions": [
                {"id": "jp_q1", "game_id": "jp_1", "game": "JP Game", "title": "セーブ 場所?", "content": "drop", "language": "jp"}
            ],
        },
        "kr_community": {
            "hot_games": [{"id": "kr_1", "name": "KR Game", "velocity": 45, "region": "kr"}],
            "player_questions": [
                {"id": "kr_q1", "game_id": "kr_1", "game": "KR Game", "title": "저장 위치?", "credentials": "drop", "language": "kr"}
            ],
        },
        "serp_snippet": {
            "hot_games": [{"id": "serp_1", "title": "Search Game", "velocity": 35}],
            "player_questions": [
                {
                    "id": "serp_q1",
                    "game_id": "serp_1",
                    "game": "Search Game",
                    "query": "best settings steam deck",
                    "snippet": "Short search snippet",
                    "authorization": "drop",
                    "table_html": "drop",
                }
            ],
        },
    }

    result = normalize_real_market_payloads(payloads)

    assert result.real_collection_performed is False
    assert result.candidate_only is True
    assert len(result.hot_games) == 5
    assert len(result.player_questions) == 5
    assert {summary.source_category for summary in result.source_summary} == set(REAL_MARKET_SOURCE_CATEGORIES)
    assert all(question.source_type in REAL_MARKET_SOURCE_CATEGORIES for question in result.player_questions)
    assert all(question.snippet is None or len(question.snippet) <= 280 for question in result.player_questions)
    forbidden = {"raw_text", "body", "selftext", "content", "credentials", "authorization", "table_html"}
    for question in result.player_questions:
        assert forbidden.isdisjoint(question.metadata)


def test_steam_market_connector_is_opt_in_and_normalizes_mock_payload(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_STEAM_DISCOVERY_URL", raising=False)
    get_settings.cache_clear()
    calls: list[dict[str, object]] = []

    def mock_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        calls.append({"url": url, "headers": headers, "timeout": timeout})
        return {
            "hot_games": [
                {
                    "app_id": "1145350",
                    "game_name": "Hades II",
                    "rank": 3,
                    "velocity": 78,
                    "community_post_velocity": 64,
                    "update_recency_days": 1,
                    "source_url": "https://steam.example/app/1145350",
                }
            ],
            "player_questions": [
                {
                    "id": "steam_q_001",
                    "game_id": "1145350",
                    "game_name": "Hades II",
                    "title": "Crash after the latest patch?",
                    "score": 240,
                    "comments": 38,
                    "growth_24h": 44,
                    "answer_maturity": "partial",
                    "snippet": "Players mention startup crashes after the latest patch.",
                    "body": "do not retain full discussion body",
                    "raw_text": "do not retain raw text",
                    "tags": ["crash", "patch"],
                }
            ],
        }

    try:
        try:
            SteamMarketConnector(http_get=mock_get).collect("Hades II")
        except RealMarketConfigError as exc:
            assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
        else:
            raise AssertionError("Steam connector should be disabled by default")
        assert calls == []

        monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
        monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
        monkeypatch.setenv("PIKO_STEAM_DISCOVERY_URL", "https://connector.example/steam")
        get_settings.cache_clear()

        result = SteamMarketConnector(http_get=mock_get).collect("Hades II", limit_per_source=3)
    finally:
        get_settings.cache_clear()

    assert result.real_collection_performed is True
    assert result.candidate_only is True
    assert len(result.hot_games) == 1
    assert len(result.player_questions) == 1
    game = result.hot_games[0]
    question = result.player_questions[0]
    assert game.steam_player_rank == 3
    assert game.update_recency_days == 1
    assert question.source_type == "steam"
    assert question.engagement_count == 240
    assert question.reply_count == 38
    assert question.growth_24h == 44
    assert {"body", "raw_text"}.isdisjoint(question.metadata)
    assert calls[0]["url"] == "https://connector.example/steam?query=Hades+II&limit=3"
    assert calls[0]["timeout"] == 5.0
    assert calls[0]["headers"]["User-Agent"].startswith("PikoBot/")


def test_reddit_and_serp_connectors_normalize_snippets_without_full_text(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_REDDIT_DISCOVERY_URL", "https://connector.example/reddit")
    monkeypatch.setenv("PIKO_SERP_DISCOVERY_URL", "https://connector.example/serp")
    get_settings.cache_clear()
    long_snippet = "search snippet " * 80

    def reddit_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "player_questions": [
                {
                    "id": "reddit_q_001",
                    "game_name": "Stardew Valley",
                    "title": "Where are saves on Windows?",
                    "url": "https://reddit.example/r/stardew/1",
                    "score": 188,
                    "comments": 29,
                    "language": "en",
                    "region": "en",
                    "snippet": "Thread title and short preview only.",
                    "selftext": "do not keep reddit selftext",
                    "body": "do not keep body",
                    "tags": ["save", "location"],
                }
            ]
        }

    def serp_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "player_questions": [
                {
                    "id": "serp_q_001",
                    "game": "Stardew Valley",
                    "query": "Stardew Valley save file location",
                    "source_title": "Search snippet source",
                    "source_url": "https://search.example/result",
                    "source": "search_snippet",
                    "language": "en",
                    "region": "global",
                    "snippet": long_snippet,
                    "content": "do not keep raw page text",
                    "full_comments": "do not keep comments",
                }
            ]
        }

    try:
        reddit_result = RedditMarketConnector(http_get=reddit_get).collect("Stardew Valley save", limit_per_source=2)
        serp_result = SERPMarketConnector(http_get=serp_get).collect("Stardew Valley save", limit_per_source=2)
    finally:
        get_settings.cache_clear()

    reddit_question = reddit_result.player_questions[0]
    serp_question = serp_result.player_questions[0]
    assert reddit_question.source_type == "reddit"
    assert reddit_question.engagement_count == 188
    assert reddit_question.reply_count == 29
    assert reddit_question.language == "en"
    assert reddit_question.source_region == "en"
    assert {"selftext", "body"}.isdisjoint(reddit_question.metadata)
    assert serp_question.source_type == "serp_snippet"
    assert serp_question.source_title == "Search snippet source"
    assert serp_question.url == "https://search.example/result"
    assert serp_question.language == "en"
    assert serp_question.source_region == "global"
    assert len(serp_question.snippet or "") <= 280
    assert {"content", "full_comments"}.isdisjoint(serp_question.metadata)
    assert search_player_needs(DiscoverySearchRequest(query="stardew save", limit=2)).real_collection_performed is False


def test_jp_and_kr_connectors_preserve_regions_and_multilingual_hints(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_JP_COMMUNITY_DISCOVERY_URL", "https://connector.example/jp")
    monkeypatch.setenv("PIKO_KR_COMMUNITY_DISCOVERY_URL", "https://connector.example/kr")
    get_settings.cache_clear()

    def jp_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "player_questions": [
                {
                    "id": "jp_q_001",
                    "game": "Stardew Valley",
                    "title": "セーブデータの場所はどこですか",
                    "language": "ja",
                    "snippet": "セーブ場所についての短い候補。",
                    "content": "全文は保存しない",
                    "tags": ["セーブ", "場所"],
                }
            ]
        }

    def kr_get(url: str, headers: dict[str, str], timeout: float) -> dict[str, object]:
        return {
            "player_questions": [
                {
                    "id": "kr_q_001",
                    "game": "Example KR Game",
                    "title": "저장 위치 오류가 있나요",
                    "language": "ko",
                    "snippet": "저장 위치와 오류에 대한 짧은 후보.",
                    "body": "본문 전체는 저장하지 않음",
                    "tags": ["저장", "위치", "오류"],
                }
            ]
        }

    try:
        jp_result = JPCommunityMarketConnector(http_get=jp_get).collect("Stardew Valley save", limit_per_source=2)
        kr_result = KRCommunityMarketConnector(http_get=kr_get).collect("save location error", limit_per_source=2)
    finally:
        get_settings.cache_clear()

    jp_question = jp_result.player_questions[0]
    kr_question = kr_result.player_questions[0]
    assert jp_question.source_region == "jp"
    assert kr_question.source_region == "kr"
    assert jp_question.language == "ja"
    assert kr_question.language == "ko"
    assert {"save", "location"}.issubset(
        set(normalization_hints_for_question(jp_question.question_text, jp_question.tags))
    )
    assert {"save", "location", "bug"}.issubset(
        set(normalization_hints_for_question(kr_question.question_text, kr_question.tags))
    )
    assert "content" not in jp_question.metadata
    assert "body" not in kr_question.metadata
    assert "translated_text" not in jp_question.metadata
    assert "translated_text" not in kr_question.metadata


class StaticDiscoveryHTTPClient:
    def __init__(self, payloads: dict[str, dict[str, object]]) -> None:
        self.payloads = payloads
        self.calls: list[dict[str, object]] = []

    def get_json(self, url: str, *, timeout: float, user_agent: str) -> dict[str, object]:
        self.calls.append({"url": url, "timeout": timeout, "user_agent": user_agent})
        return self.payloads[url]


def test_broad_real_market_discovery_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    get_settings.cache_clear()
    try:
        source = RealMarketDiscoverySource(
            [RealDiscoveryEndpoint("steam", "steam_discussion", "global", "https://example.invalid/steam")],
            client=StaticDiscoveryHTTPClient({}),
        )
        try:
            source.collect("Hades II")
        except DiscoveryRealSourceDisabledError as exc:
            assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in str(exc)
        else:
            raise AssertionError("broad real source discovery should be disabled by default")
    finally:
        get_settings.cache_clear()


def test_broad_real_market_discovery_requires_configured_endpoints(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    get_settings.cache_clear()
    try:
        source = RealMarketDiscoverySource([], client=StaticDiscoveryHTTPClient({}))
        try:
            source.collect("Hades II")
        except DiscoveryRealSourceConfigurationError as exc:
            assert "PIKO_STEAM_DISCOVERY_URL" in str(exc)
        else:
            raise AssertionError("real source discovery should require at least one endpoint")
    finally:
        get_settings.cache_clear()


def test_broad_real_market_discovery_normalizes_steam_reddit_jp_kr_without_raw_text(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    get_settings.cache_clear()
    endpoints = [
        RealDiscoveryEndpoint("steam", "steam_discussion", "global", "https://example.invalid/steam"),
        RealDiscoveryEndpoint("reddit", "reddit", "global", "https://example.invalid/reddit"),
        RealDiscoveryEndpoint("jp_community", "jp_community", "jp", "https://example.invalid/jp"),
        RealDiscoveryEndpoint("kr_community", "kr_community", "kr", "https://example.invalid/kr"),
    ]
    client = StaticDiscoveryHTTPClient(
        {
            "https://example.invalid/steam": {
                "games": [
                    {
                        "app_id": "1145350",
                        "game_name": "Hades II",
                        "rank": 12,
                        "community_post_velocity": 92,
                        "update_recency_days": 2,
                    }
                ],
                "questions": [
                    {
                        "thread_id": "steam_001",
                        "game_id": "hades_ii",
                        "game_name": "Hades II",
                        "title": "Hades II crashes after the latest patch",
                        "url": "https://example.invalid/steam/thread/1",
                        "engagement_count": 300,
                        "comment_count": 55,
                        "growth_24h": 80,
                        "evidence_quality": 35,
                        "tags": ["crash", "patch"],
                        "raw_text": "must not be retained",
                        "snippet": "Players report crashes after the latest patch.",
                    }
                ],
            },
            "https://example.invalid/reddit": {
                "games": [],
                "questions": [
                    {
                        "id": "reddit_001",
                        "game_name": "Hades II",
                        "title": "Any reliable 40 FPS Steam Deck settings?",
                        "permalink": "https://example.invalid/r/hades/1",
                        "score": 128,
                        "num_comments": 24,
                        "has_accepted_answer": True,
                        "evidence_quality": 62,
                        "source_region": "en",
                        "tags": ["settings", "steam_deck"],
                    }
                ],
            },
            "https://example.invalid/jp": {
                "games": [],
                "questions": [
                    {
                        "question_id": "jp_001",
                        "game_name": "Stardew Valley",
                        "question_text": "セーブデータの場所はどこですか？",
                        "source_region": "jp",
                        "language": "jp",
                        "engagement_count": 90,
                        "reply_count": 7,
                        "has_accepted_answer": True,
                        "evidence_quality": 70,
                        "tags": ["save", "location"],
                    }
                ],
            },
            "https://example.invalid/kr": {
                "games": [],
                "questions": [
                    {
                        "question_id": "kr_001",
                        "game_name": "Example KR Game",
                        "question_text": "저장 위치가 어디인가요?",
                        "source_region": "kr",
                        "language": "kr",
                        "engagement_count": 60,
                        "reply_count": 4,
                        "evidence_quality": 58,
                        "tags": ["save", "location"],
                    }
                ],
            },
        }
    )
    try:
        result = RealMarketDiscoverySource(endpoints, client=client).collect("Hades II", limit_per_source=10)
    finally:
        get_settings.cache_clear()

    assert result["status"] == "completed"
    assert result["mode"] == "real-source"
    assert result["real_collection_performed"] is True
    assert result["publishing_performed"] is False
    assert len(result["sources"]) == 4
    assert len(result["games"]) == 1
    assert len(result["questions"]) == 4
    source_types = {question["source_type"] for question in result["questions"]}
    assert {"steam_discussion", "reddit", "jp_community", "kr_community"}.issubset(source_types)
    regions = {question["source_region"] for question in result["questions"]}
    assert {"global", "en", "jp", "kr"}.issubset(regions)
    assert all(len(question.get("snippet") or "") <= 500 for question in result["questions"])
    assert all(question["metadata"]["raw_text_included"] is False for question in result["questions"])
    assert all("raw_text" not in question["metadata"] for question in result["questions"])
    assert len(client.calls) == 4


def test_discovery_real_source_api_is_opt_in_only(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    get_settings.cache_clear()
    try:
        response = client.post("/discovery/real-source/collect", json={"query": "Hades II", "limit_per_source": 3})
        assert response.status_code == 403
        assert "PIKO_ENABLE_DISCOVERY_REAL_SOURCE=true" in response.json()["detail"]
    finally:
        get_settings.cache_clear()


def test_hot_strategy_rankings_cover_games_audience_types_and_safety() -> None:
    result = hot_strategy_rankings(limit=5)

    assert result["status"] == "completed"
    assert result["mode"] == "fixture"
    assert result["real_collection_performed"] is False
    assert result["top_hot_games"]
    assert len(result["top_hot_games"]) <= 5
    assert result["top_guide_needs"]
    assert result["audience_rankings"]
    assert result["game_type_rankings"]
    assert result["decision_rankings"]
    assert "不是对真实玩家性别做判断" in result["methodology"]
    assert all("guide_need_score" in row for row in result["top_hot_games"])
    assert any(row["profile_id"] == "female_interest_fit" for row in result["audience_rankings"])
    assert any(row["profile_id"] == "male_interest_fit" for row in result["audience_rankings"])


def test_real_market_hot_game_ranking_prefers_recent_high_velocity_games() -> None:
    rows = rank_hot_games(
        [
            GameHeatSignal(
                game_id="old_slow",
                game_name="Old Slow Game",
                region_signals=["steam"],
                steam_player_rank=90,
                steam_review_velocity=5,
                community_post_velocity=6,
                update_recency_days=120,
                cross_region_mentions=0,
            ),
            GameHeatSignal(
                game_id="fresh_fast",
                game_name="Fresh Fast Game",
                region_signals=["steam", "reddit", "jp"],
                steam_player_rank=12,
                steam_review_velocity=88,
                community_post_velocity=92,
                update_recency_days=2,
                cross_region_mentions=3,
            ),
            GameHeatSignal(
                game_id="mid_game",
                game_name="Mid Game",
                region_signals=["steam", "serp"],
                steam_player_rank=40,
                steam_review_velocity=45,
                community_post_velocity=40,
                update_recency_days=30,
                cross_region_mentions=1,
            ),
        ],
        mode="fixture",
        limit=2,
    )

    assert len(rows) == 2
    assert rows[0]["game_id"] == "fresh_fast"
    assert rows[0]["mode"] == "fixture"
    assert rows[0]["source_diversity"] == 3
    assert rows[0]["ranking_score"] > rows[1]["ranking_score"]
    assert all(row["candidate_only"] is True for row in rows)


def test_real_market_rankings_expose_top_games_and_question_buckets() -> None:
    result = hot_strategy_rankings(limit=5)
    buckets = result["question_ranking_buckets"]

    assert result["mode"] == "fixture"
    assert result["real_collection_performed"] is False
    assert result["publish_ready"] is False
    assert result["publishing_performed"] is False
    assert 1 <= len(result["real_market_hot_games_top_5"]) <= 5
    assert len(result["real_market_hot_games_top_20"]) <= 20
    assert {"ranking_score", "source_diversity", "discussion_velocity"}.issubset(result["real_market_hot_games_top_5"][0])
    assert {
        "hot_answered_questions",
        "hot_unanswered_watchlist_questions",
        "conflict_answer_topics",
        "high_risk_blocked_topics",
        "must_check_guide_topics",
    }.issubset(buckets)
    assert buckets["hot_answered_questions"]
    assert buckets["hot_unanswered_watchlist_questions"]
    assert buckets["conflict_answer_topics"]
    assert buckets["high_risk_blocked_topics"]
    assert buckets["must_check_guide_topics"]

    required = {
        "decision",
        "intent",
        "evidence_quality",
        "heat",
        "answer_status",
        "risk",
        "recommended_next_action",
    }
    assert required.issubset(buckets["must_check_guide_topics"][0])
    assert all(row["risk"] != "high" for row in buckets["must_check_guide_topics"])
    assert all(row["decision"] != "publish_candidate" for row in buckets["high_risk_blocked_topics"])
    assert all(row["publish_ready"] is False for row in buckets["high_risk_blocked_topics"])
    assert all(row["runnable"] is False for row in buckets["hot_unanswered_watchlist_questions"])


def test_discovery_rankings_api_and_window_surface() -> None:
    response = client.get("/discovery/rankings?limit=5")

    assert response.status_code == 200
    payload = response.json()
    assert payload["top_hot_games"]
    assert payload["top_guide_needs"]
    assert payload["real_market_hot_games_top_5"]
    assert payload["question_ranking_buckets"]["must_check_guide_topics"]
    assert payload["real_collection_performed"] is False

    window = client.get("/discovery/window")
    assert window.status_code == 200
    assert "当前攻略机会热榜 Top 5" in window.text
    assert "Current hot games Top 5" in window.text
    assert "Must-check guide topics" in window.text
    assert "Conflict answer topics" in window.text
    assert "High-risk blocked topics" in window.text
    assert "游戏类型排行榜" in window.text
    assert "玩家画像/兴趣画像排行榜" in window.text
    assert "必须查攻略的问题排行" in window.text
    assert "已有答案 / 未解决高热问题" in window.text
    assert "冲突答案榜" in window.text
    assert "高风险阻断榜" in window.text
    assert "Ranking mode" in window.text
    assert "/discovery/rankings" in window.text


def test_discovery_funnel_trace_exposes_step_by_step_actions() -> None:
    trace = discovery_funnel_trace(DiscoverySearchRequest(min_game_heat=50, limit=20))

    assert trace["status"] == "completed"
    assert trace["mode"] == "fixture"
    assert trace["real_collection_performed"] is False
    assert trace["publish_ready"] is False
    assert trace["publishing_performed"] is False
    assert trace["summary"]["raw_game_count"] >= 1
    assert trace["summary"]["raw_question_count"] >= 1
    assert trace["summary"]["cluster_count"] >= 1
    assert len(trace["steps"]) == 6

    source_scan = trace["steps"][0]
    platforms = [item["platform"] for item in source_scan["outputs"]["platforms"]]
    assert {"Steam", "Reddit", "SERP snippets", "JP community", "KR community"}.issubset(platforms)
    assert any("No crawler" in guardrail for guardrail in source_scan["guardrails"])

    routing = trace["steps"][4]
    assert routing["outputs"]["publish_candidates"]
    assert routing["outputs"]["watchlist"]
    assert routing["outputs"]["conflict_explainers"]
    assert routing["outputs"]["high_risk_blocked"]
    assert all(item["publish_ready"] is False for item in routing["outputs"]["publish_candidates"])
    assert all(item["requires_evidence_pipeline"] is True for item in routing["outputs"]["publish_candidates"])

    solution_path = trace["steps"][5]
    assert "WriterAgent" in solution_path["outputs"]["planned_agent_path"]
    assert "VerificationGate" in solution_path["outputs"]["planned_agent_path"]


def test_discovery_funnel_trace_api_and_window_surface() -> None:
    response = client.post("/discovery/funnel-trace", json={"min_game_heat": 50, "limit": 20})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["steps"][0]["title"] == "大范围来源扫描"
    assert payload["steps"][4]["title"] == "漏斗分流"
    assert payload["real_collection_performed"] is False

    window = client.get("/discovery/funnel-window")
    assert window.status_code == 200
    assert "Piko 漏斗透明窗口" in window.text
    assert "大范围市场信号" in window.text
    assert "/discovery/funnel-trace" in window.text
    assert "默认不触网" in window.text
