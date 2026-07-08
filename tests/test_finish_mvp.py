import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.final_mvp.pipeline import (
    BLOCKED_FOR_EXTERNAL_ENDPOINT,
    LATEST_CONTENT_PACKAGE,
    LATEST_EXTERNAL_LIVE_RESULT,
    LATEST_MVP_READINESS,
    LATEST_OPERATOR_CONSOLE,
    LATEST_PUBLISH_DISTRIBUTION_PLAN,
    LATEST_REAL_SIGNAL_FUNNEL,
    build_finish_gate_artifacts,
    external_live_result,
)
from packages.shared.config import get_settings


client = TestClient(app)


def test_finish_missing_external_endpoint_is_blocked(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    result = external_live_result()
    assert result["status"] == BLOCKED_FOR_EXTERNAL_ENDPOINT
    assert result["real_collection_performed"] is False
    assert result["endpoint_url_present"] is False
    assert result["blocked_reason"] in {"missing_external_endpoint_url", "missing_required_opt_in"}
    assert result["publishing_performed"] is False
    assert result["broad_internet_coverage"] is False


def test_finish_localhost_endpoint_cannot_be_external_success(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", "true")
    monkeypatch.setenv("PIKO_LIVE_DISCOVERY_TEST", "true")
    monkeypatch.setenv("PIKO_APPROVED_ENDPOINT_URL", "http://127.0.0.1:8765/approved-market.json")
    get_settings.cache_clear()
    result = external_live_result()
    assert result["status"] == BLOCKED_FOR_EXTERNAL_ENDPOINT
    assert result["real_collection_performed"] is False
    assert result["blocked_reason"] == "localhost_not_allowed_for_external_endpoint"
    assert result["endpoint_url_stored"] is False


def test_finish_artifact_parse_and_safety_fields(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    artifacts = build_finish_gate_artifacts()
    assert artifacts["external_live_result"]["status"] == BLOCKED_FOR_EXTERNAL_ENDPOINT
    payload = json.loads(LATEST_EXTERNAL_LIVE_RESULT.read_text(encoding="utf-8"))
    assert payload["real_collection_performed"] is False
    unsafe_true = {
        "raw_response_body_saved",
        "full_posts_saved",
        "full_pages_saved",
        "full_comments_saved",
        "credentials_stored",
        "secrets_retained",
        "crawler_used",
        "html_scrape_used",
        "llm_called",
        "broad_internet_coverage",
        "publish_ready",
        "publishing_performed",
        "upload_performed",
        "deployment_performed",
    }
    for key in unsafe_true:
        assert payload[key] is False
    assert Path(LATEST_EXTERNAL_LIVE_RESULT).exists()


def test_finish_external_success_artifacts_from_mocked_probe(monkeypatch) -> None:
    external = {
        "readiness": {
            "status": "ready",
            "missing_config": [],
            "endpoint_url_present": True,
            "endpoint_scheme": "https",
            "endpoint_host": "example.com",
            "double_opt_in_configured": True,
        },
        "probe": {
            "status": "success",
            "real_collection_performed": True,
            "normalized_game_count": 1,
            "normalized_question_count": 1,
            "retained_fields": ["games", "questions", "snippet"],
            "ranking_preview": {
                "top_hot_games": [{"game_id": "hades_ii", "game_name": "Hades II", "candidate_only": True}]
            },
        },
        "handoff": {
            "source_trace": [{"scope": "external_approved_endpoint", "status": "success", "source_id": "approved_1"}],
            "pain_buckets": {
                "hot_answered_questions": [
                    {
                        "question_id": "q1",
                        "game_name": "Hades II",
                        "question_text": "Where is the save file?",
                        "evidence_quality": 70,
                        "risk_level": "low",
                        "publish_ready": False,
                    }
                ]
            },
        },
        "candidate_package": {
            "selected_topic": {
                "question_id": "q1",
                "game_name": "Hades II",
                "question_text": "Where is the save file?",
                "evidence_quality": 70,
                "risk_level": "low",
                "publish_ready": False,
            },
            "source_trace": [{"scope": "external_approved_endpoint", "status": "success", "source_id": "approved_1"}],
        },
    }
    monkeypatch.setattr("packages.final_mvp.pipeline.build_external_endpoint_artifacts", lambda: external)
    artifacts = build_finish_gate_artifacts()
    assert artifacts["external_live_result"]["real_collection_performed"] is True
    assert artifacts["real_signal_funnel"]["domain_routing"]["routing_decision"] == "route_to_gaming_domain_pack"
    assert artifacts["content_package"]["publish_ready"] is False
    assert artifacts["content_package"]["publishing_performed"] is False
    assert artifacts["operator_console"]["read_only_surface"] is True
    assert artifacts["publish_distribution_plan"]["publishing_performed"] is False
    assert artifacts["mvp_readiness"]["status"] == "mvp_ready_for_verify"
    assert artifacts["mvp_readiness"]["publishing_performed"] is False
    for path in [
        LATEST_EXTERNAL_LIVE_RESULT,
        LATEST_REAL_SIGNAL_FUNNEL,
        LATEST_CONTENT_PACKAGE,
        LATEST_OPERATOR_CONSOLE,
        LATEST_PUBLISH_DISTRIBUTION_PLAN,
        LATEST_MVP_READINESS,
    ]:
        assert Path(path).exists()
        json.loads(Path(path).read_text(encoding="utf-8"))


def test_finish_operator_api_and_window_are_read_only(monkeypatch) -> None:
    monkeypatch.delenv("PIKO_ENABLE_DISCOVERY_REAL_SOURCE", raising=False)
    monkeypatch.delenv("PIKO_LIVE_DISCOVERY_TEST", raising=False)
    monkeypatch.delenv("PIKO_APPROVED_ENDPOINT_URL", raising=False)
    get_settings.cache_clear()
    result = client.get("/final-mvp/result")
    window = client.get("/final-mvp/window")
    assert result.status_code == 200
    assert result.json()["external_live_result"]["real_collection_performed"] is False
    assert window.status_code == 200
    assert "No publish, upload, deploy" in window.text
