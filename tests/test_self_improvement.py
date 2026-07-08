from copy import deepcopy

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.improvement.diagnostics import diagnostic_from_verification_report
from packages.improvement.patch_plan import patch_plan_from_proposal
from packages.improvement.proposal_agent import proposal_from_diagnostic
from packages.improvement.regression_runner import default_regression_plan
from packages.improvement.upgrade_ledger import LedgerGuardrailError, append_ledger_entry, make_ledger_entry
from packages.improvement.workflow_integration import generate_improvement_report_from_workflow
from packages.shared.schemas import (
    DiagnosticReport,
    ImprovementSignal,
    PatchPlan,
    UpgradeLedgerEntry,
    UpgradeProposal,
    VerificationStatus,
    WorkflowStartRequest,
)
from packages.workflows.article_pipeline import run_article_pipeline
from packages.workflows.verification import verify_workflow_report


client = TestClient(app)


def test_improvement_schemas_round_trip() -> None:
    signal = ImprovementSignal(
        signal_id="signal_test",
        priority="high",
        failed_check="evidence_source_trace",
        suggested_fix="Restore source_id traceability.",
        affected_module="packages/indexing/evidence_extractor.py",
    )
    diagnostic = DiagnosticReport(diagnostic_id="diagnostic_test", status="needs_improvement", signals=[signal])
    proposal = UpgradeProposal(
        proposal_id="proposal_test",
        diagnostic_id=diagnostic.diagnostic_id,
        title="Fix traceability",
        reason="Evidence source trace failed.",
        affected_modules=["packages/indexing/evidence_extractor.py"],
        expected_benefit="Restore verification pass.",
        required_tests=["python -m pytest"],
    )
    patch_plan = PatchPlan(
        plan_id="plan_test",
        proposal_id=proposal.proposal_id,
        summary="Plan only.",
        regression_commands=default_regression_plan(),
    )
    ledger = make_ledger_entry(proposal, patch_plan)

    assert DiagnosticReport.model_validate(diagnostic.model_dump()).signals[0].signal_id == "signal_test"
    assert UpgradeLedgerEntry.model_validate(ledger.model_dump()).patch_plan.auto_apply_allowed is False


def test_failed_verification_generates_diagnostic_proposal_patch_plan() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    broken = deepcopy(report)
    broken.pipeline_state.evidence_cards[0].source_id = "missing_source"
    verification = verify_workflow_report(broken)

    diagnostic = diagnostic_from_verification_report(verification)
    proposal = proposal_from_diagnostic(diagnostic)
    patch_plan = patch_plan_from_proposal(proposal)

    assert verification.status == VerificationStatus.failed
    assert diagnostic.status == "needs_improvement"
    assert diagnostic.signals
    assert proposal.auto_apply_allowed is False
    assert proposal.requires_operator_decision is True
    assert patch_plan.auto_apply_allowed is False
    assert any(command.command == "python -m pytest" for command in patch_plan.regression_commands)


def test_passed_verification_generates_noop_report_without_publish_mutation() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    original_publish_decision = report.publish_decision

    bundle = generate_improvement_report_from_workflow(report)

    assert bundle["diagnostic_report"].status == "no_action"
    assert bundle["upgrade_proposal"].title == "No-op improvement proposal"
    assert bundle["auto_apply_performed"] is False
    assert bundle["regression_executed"] is False
    assert bundle["publishing_state_mutated"] is False
    assert report.publish_decision == original_publish_decision


def test_improvement_api_failed_report_returns_proposal_and_plan() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    report.pipeline_state.evidence_cards = []
    verification = verify_workflow_report(report)

    response = client.post("/improvement/from-verification-report", json=verification.model_dump(mode="json"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["diagnostic_report"]["status"] == "needs_improvement"
    assert payload["upgrade_proposal"]["auto_apply_allowed"] is False
    assert payload["patch_plan"]["auto_apply_allowed"] is False
    assert payload["regression_executed"] is False


def test_improvement_api_from_workflow_report_does_not_mutate_publish_state() -> None:
    report = run_article_pipeline(WorkflowStartRequest())
    response = client.post("/improvement/from-workflow-report", json=report.model_dump(mode="json"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["publishing_state_mutated"] is False
    assert payload["patch_plan"]["regression_commands"]
    assert report.publish_decision is not None
    assert report.publish_decision.value == "verified_candidate"


def test_ledger_entry_writes_normal_jsonl(tmp_path) -> None:
    entry = _sample_ledger_entry()
    target = tmp_path / "upgrade_ledger.jsonl"

    append_ledger_entry(entry, str(target))

    lines = target.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert "proposal_test" in lines[0]


def test_ledger_guardrail_rejects_secret_field(tmp_path) -> None:
    payload = _sample_ledger_entry().model_dump(mode="json")
    payload["metadata"] = {"secret": "do-not-write"}

    try:
        append_ledger_entry(payload, str(tmp_path / "upgrade_ledger.jsonl"))
    except LedgerGuardrailError as exc:
        assert "prohibited field 'secret'" in str(exc)
    else:
        raise AssertionError("Expected LedgerGuardrailError")


def test_ledger_guardrail_rejects_raw_text_field(tmp_path) -> None:
    payload = _sample_ledger_entry().model_dump(mode="json")
    payload["source"] = {"raw_text": "long source body"}

    try:
        append_ledger_entry(payload, str(tmp_path / "upgrade_ledger.jsonl"))
    except LedgerGuardrailError as exc:
        assert "prohibited field 'raw_text'" in str(exc)
    else:
        raise AssertionError("Expected LedgerGuardrailError")


def test_ledger_guardrail_truncates_long_snippet_with_warning(tmp_path) -> None:
    payload = _sample_ledger_entry().model_dump(mode="json")
    payload["source"] = {"snippet": "x" * 2500}
    target = tmp_path / "upgrade_ledger.jsonl"

    append_ledger_entry(payload, str(target))

    written = target.read_text(encoding="utf-8")
    assert "x" * 2000 in written
    assert "x" * 2001 not in written
    assert "Ledger guardrail: truncated long string at $.source.snippet from 2500 to 2000 characters" in written


def _sample_ledger_entry():
    proposal = UpgradeProposal(
        proposal_id="proposal_test",
        diagnostic_id="diagnostic_test",
        title="Fix traceability",
        reason="Evidence source trace failed.",
        affected_modules=["packages/indexing/evidence_extractor.py"],
        expected_benefit="Restore verification pass.",
        required_tests=["python -m pytest"],
    )
    patch_plan = PatchPlan(
        plan_id="plan_test",
        proposal_id=proposal.proposal_id,
        summary="Plan only.",
        regression_commands=default_regression_plan(),
    )
    return make_ledger_entry(proposal, patch_plan)
