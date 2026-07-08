from copy import deepcopy

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.shared.schemas import VerificationStatus, WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline
from packages.workflows.verification import verify_workflow_report


client = TestClient(app)


def test_valid_workflow_report_passes_verification() -> None:
    report = run_article_pipeline(WorkflowStartRequest())

    assert report.verification_report is not None
    assert report.verification_report.status == VerificationStatus.passed
    assert report.pipeline_state.verification_report is not None


def test_verifier_fails_missing_evidence() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    report.pipeline_state.evidence_cards = []

    verification = verify_workflow_report(report)

    assert verification.status == VerificationStatus.failed
    assert any(check.name == "evidence_source_trace" and check.status == VerificationStatus.failed for check in verification.checks)


def test_verifier_catches_source_id_mismatch() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    report.pipeline_state.evidence_cards[0].source_id = "missing_source"

    verification = verify_workflow_report(report)

    assert verification.status == VerificationStatus.failed
    assert any("missing_source" in check.details.get("missing_source_ids", []) for check in verification.checks)


def test_verifier_catches_publish_ready_with_failed_gates() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    mutated = deepcopy(report)
    mutated.pipeline_state.gate_results[0].result.decision = "fail"
    if mutated.publish_decision:
        mutated.publish_decision.blocks_publish = False

    verification = verify_workflow_report(mutated)

    assert verification.status == VerificationStatus.failed
    assert any(check.name == "gate_decision_consistency" for check in verification.checks)


def test_verification_api_accepts_passing_and_failing_reports() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    passing_response = client.post("/workflow/article/verify", json=report.model_dump(mode="json"))
    assert passing_response.status_code == 200
    assert passing_response.json()["status"] == "pass"

    report.pipeline_state.evidence_cards = []
    failing_response = client.post("/workflow/article/verify", json=report.model_dump(mode="json"))
    assert failing_response.status_code == 200
    assert failing_response.json()["status"] == "fail"
