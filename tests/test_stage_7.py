from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.gates.publishing_eligibility import evaluate_publishing_eligibility
from packages.shared.schemas import WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline


client = TestClient(app)


def test_public_guide_template_contains_source_box() -> None:
    html = Path("apps/web/pages/guide-template.html").read_text(encoding="utf-8")

    assert "Sources Checked" in html
    assert "fixture_official_launch_001" in html
    assert "Risk: Low" in html


def test_publishing_eligibility_is_explicit_and_does_not_deploy() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    eligibility = evaluate_publishing_eligibility(report)

    assert eligibility.eligible is True
    assert eligibility.deploy_performed is False


def test_publishing_eligibility_api_blocks_failed_verification() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    report.verification_report = None
    response = client.post("/workflow/article/eligibility", json=report.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.json()["eligible"] is False
    assert response.json()["deploy_performed"] is False


def test_feedback_endpoint_stores_signal_only() -> None:
    response = client.post(
        "/feedback",
        json={
            "article_id": "article_mock_001",
            "helpful": False,
            "did_not_work": True,
            "comment": "Step 2 did not help.",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["stored_as_signal_only"] is True
    assert payload["feedback_id"].startswith("feedback_")


def test_invalid_feedback_is_rejected() -> None:
    response = client.post("/feedback", json={"helpful": True})

    assert response.status_code == 422
