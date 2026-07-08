import json

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.discovery.real_endpoint_verify import verify_fixture, write_endpoint_verification_artifact
from packages.discovery.rev_pipeline import (
    approved_live_source_registry,
    endpoint_fed_rankings,
    operator_result_surface,
    run_real_search_endpoint_adapter,
    selected_safe_topic_candidate,
    source_hints_and_evidence_readiness,
    write_latest_real_market_funnel_report,
    write_publish_readiness_metadata,
    write_source_backed_article_package,
)


client = TestClient(app)


def test_rev3_approved_live_source_registry_is_default_disabled() -> None:
    registry = approved_live_source_registry()

    assert registry["status"] == "completed"
    assert registry["default_network_disabled"] is True
    assert registry["approved_endpoint_types"] == ["json"]
    assert "html" in registry["rejected_endpoint_types"]
    categories = {source["source_category"] for source in registry["sources"]}
    assert {"steam", "reddit", "serp_snippet", "jp_community", "kr_community"}.issubset(categories)
    assert all(source["enabled_by_default"] is False for source in registry["sources"])
    assert all(source["endpoint_type"] == "json" for source in registry["sources"])
    assert all("raw_text" in source["prohibited_fields"] for source in registry["sources"])


def test_rev3_real_search_adapter_fixture_and_live_skip_are_safe() -> None:
    fixture = run_real_search_endpoint_adapter(mode="fixture", limit=3)
    live = run_real_search_endpoint_adapter(mode="live", limit=3)

    assert fixture["status"] == "completed"
    assert fixture["mode"] == "fixture"
    assert fixture["games"]
    assert fixture["questions"]
    assert fixture["real_collection_performed"] is False
    assert fixture["discarded_count"] == 0
    assert fixture["unsupported_record_count"] == 0
    assert fixture["source_trace"][0]["normalized_count"] >= 1
    assert live["status"] == "skipped"
    assert live["real_collection_performed"] is False
    assert live["skip_reason"]
    assert all("raw_text" not in json.dumps(question, ensure_ascii=False) for question in fixture["questions"])


def test_rev3_endpoint_trace_api_and_artifact_surface() -> None:
    path = write_endpoint_verification_artifact(verify_fixture())
    payload = json.loads(path.read_text(encoding="utf-8"))
    response = client.get("/discovery/funnel-trace")
    window = client.get("/discovery/funnel-window")

    assert payload["artifact_type"] == "endpoint_verification_summary"
    assert payload["raw_response_body_saved"] is False
    assert response.status_code == 200
    assert response.json()["steps"][0]["outputs"]["mode"] == "fixture"
    assert window.status_code == 200
    assert "/discovery/funnel-trace" in window.text
    assert response.json()["publishing_performed"] is False


def test_rev4_endpoint_fed_rankings_and_api_surface_are_candidate_only() -> None:
    rankings = endpoint_fed_rankings(mode="mock-live", limit=5)
    response = client.get("/discovery/endpoint-rankings?mode=mock-live&limit=5")

    assert rankings["status"] == "completed"
    assert rankings["mode"] == "mock-live"
    assert rankings["real_collection_performed"] is False
    assert rankings["real_market_hot_games_top_5"]
    assert len(rankings["real_market_hot_games_top_20"]) <= 20
    assert {"ranking_score", "source_diversity", "discussion_velocity"}.issubset(
        rankings["real_market_hot_games_top_5"][0]
    )
    buckets = rankings["question_ranking_buckets"]
    assert buckets["hot_answered_questions"]
    assert buckets["hot_unanswered_watchlist_questions"]
    assert buckets["conflict_answer_topics"]
    assert buckets["high_risk_blocked_topics"]
    assert all(row["runnable"] is False for row in buckets["hot_unanswered_watchlist_questions"])
    assert all(row["publish_ready"] is False for row in buckets["high_risk_blocked_topics"])
    assert response.status_code == 200
    assert response.json()["mode"] == "mock-live"


def test_rev5_safe_topic_candidate_hints_and_funnel_report(tmp_path, monkeypatch) -> None:
    selected = selected_safe_topic_candidate()
    hints = source_hints_and_evidence_readiness()
    monkeypatch.setattr("packages.discovery.rev_pipeline.LATEST_FUNNEL_REPORT_PATH", tmp_path / "report.json")
    report_path = write_latest_real_market_funnel_report()
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert selected["status"] == "completed"
    assert selected["candidate"]["decision"] == "publish_candidate"
    assert selected["candidate"]["publish_ready"] is False
    assert selected["candidate"]["requires_evidence_pipeline"] is True
    assert selected["blocked_examples"]
    assert any(item["decision"] != "publish_candidate" for item in selected["blocked_examples"])
    assert hints["source_query_hints"]
    assert hints["evidence_readiness"]["needs_page_level_evidence"] is True
    assert report["artifact_type"] == "latest_real_market_funnel_report"
    assert report["publish_ready"] is False
    assert report["publishing_performed"] is False
    serialized = json.dumps(report, ensure_ascii=False)
    assert "raw_text" not in serialized
    assert "authorization" not in serialized
    assert "api_key" not in serialized


def test_rev6_article_package_publish_readiness_and_operator_surface(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("packages.discovery.rev_pipeline.LATEST_ARTICLE_PACKAGE_PATH", tmp_path / "article.json")
    monkeypatch.setattr("packages.discovery.rev_pipeline.LATEST_ARTICLE_PACKAGE_MD_PATH", tmp_path / "article.md")
    monkeypatch.setattr("packages.discovery.rev_pipeline.LATEST_PUBLISH_READINESS_PATH", tmp_path / "readiness.json")
    monkeypatch.setattr("packages.discovery.rev_pipeline.LATEST_FUNNEL_REPORT_PATH", tmp_path / "report.json")

    write_latest_real_market_funnel_report()
    article_json, article_md = write_source_backed_article_package()
    readiness_path = write_publish_readiness_metadata()
    surface = operator_result_surface()

    article = json.loads(article_json.read_text(encoding="utf-8"))
    readiness = json.loads(readiness_path.read_text(encoding="utf-8"))
    assert article_json.exists()
    assert article_md.exists()
    assert article["artifact_type"] == "source_backed_article_package"
    assert article["publish_ready"] is False
    assert article["publishing_performed"] is False
    assert article["source_trace_present"] is True
    assert "verification_report" in article
    assert readiness["media_plan_present"] is True
    assert readiness["has_images"] is False
    assert readiness["publishing_performed"] is False
    assert readiness["media_plan"]["image_source_policy"].startswith("Do not download")
    assert surface["status"] == "completed"
    assert surface["article_package"].endswith("article.json")
    assert surface["publishing_performed"] is False
