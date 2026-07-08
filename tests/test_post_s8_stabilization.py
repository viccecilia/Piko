import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from packages.collectors.base import DisabledConnectorError
from packages.collectors.mediawiki import MediaWikiConnector
from packages.shared.config import get_settings


client = TestClient(app)


def test_article_run_api_exposes_verification_and_decision_fields() -> None:
    response = client.post(
        "/workflow/article/run",
        json={
            "game_id": "game_mock_001",
            "game_name": "Example Game",
            "player_question": "crash on startup",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["verification_report"]["status"] == "pass"
    assert payload["pipeline_state"]["verification_report"]["status"] == "pass"
    assert payload["publish_action"] == "draft_review"
    assert payload["publish_decision"]["value"] == "verified_candidate"
    assert "Stage 1" not in payload["publish_decision"]["recommended_next_action"]


def test_publishing_eligibility_api_never_deploys() -> None:
    workflow_response = client.post(
        "/workflow/article/run",
        json={
            "game_id": "game_mock_001",
            "game_name": "Example Game",
            "player_question": "crash on startup",
        },
    )
    eligibility_response = client.post("/workflow/article/eligibility", json=workflow_response.json())

    assert eligibility_response.status_code == 200
    assert eligibility_response.json()["deploy_performed"] is False


def test_real_connector_default_path_is_disabled() -> None:
    assert get_settings().enable_real_connectors is False
    with pytest.raises(DisabledConnectorError):
        MediaWikiConnector().search("Example Game")


def test_delivery_docs_name_current_commands_and_safety_defaults() -> None:
    readme = open("README.md", encoding="utf-8").read()
    current_state = open("docs/current_state.md", encoding="utf-8").read()

    assert "python -m uvicorn apps.api.main:app --reload" in readme
    assert "python -m pytest" in readme
    assert "PIKO_ENABLE_REAL_CONNECTORS=false" in readme
    assert "POST /workflow/article/verify" in current_state
    assert "deploy_performed" in current_state
