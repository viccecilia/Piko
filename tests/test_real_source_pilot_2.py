import json
import os
from pathlib import Path

import pytest

from packages.collectors.base import ConnectorSearchResult
from packages.indexing.evidence_extractor import extract_evidence_cards_from_source_records
from packages.shared.config import get_settings
from packages.shared.schemas import PublishDecisionValue, VerificationStatus, WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline
from packages.workflows.verification import verify_workflow_report


def _pilot_1_records() -> list[dict[str, object]]:
    sample = json.loads(Path(".piko/summaries/real_source_pilot_1_sample.json").read_text(encoding="utf-8"))
    return sample["records"]


def test_real_source_records_generate_traceable_candidate_evidence_cards() -> None:
    cards = extract_evidence_cards_from_source_records(_pilot_1_records())

    assert cards
    assert all(card["source_id"].startswith("pcgamingwiki_") for card in cards)
    assert all(card["claim_type"] == "source_candidate" for card in cards)
    assert all(card["solution"] is None for card in cards)
    assert all(card["uncertainty"] == "needs_more_evidence" for card in cards)
    assert all(len(str(card["quote_snippet"])) <= 300 for card in cards)


def test_verification_fails_when_real_evidence_source_id_is_not_traceable(monkeypatch: pytest.MonkeyPatch) -> None:
    report = _run_mocked_real_source_workflow(monkeypatch)
    report.pipeline_state.sources = []

    verification = verify_workflow_report(report)

    assert verification.status == VerificationStatus.failed
    trace_check = next(check for check in verification.checks if check.name == "evidence_source_trace")
    assert trace_check.status == VerificationStatus.failed
    assert trace_check.details["missing_source_ids"]


def test_mocked_real_source_workflow_needs_more_evidence_not_publish_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    report = _run_mocked_real_source_workflow(monkeypatch)

    assert report.agent_outputs["source_agent"]["real_collection_performed"] is True
    assert report.agent_outputs["evidence_agent"]["real_source_records_used"] is True
    assert report.pipeline_state.sources
    assert report.pipeline_state.evidence_cards
    assert all(card.source_id.startswith("pcgamingwiki_") for card in report.pipeline_state.evidence_cards)
    assert report.pipeline_state.ranked_steps == []
    assert report.publish_decision is not None
    assert report.publish_decision.value == PublishDecisionValue.needs_more_evidence
    assert report.publish_decision.blocks_publish is True
    assert report.publish_action == "discard"

    evidence_trace = next(check for check in report.verification_report.checks if check.name == "evidence_source_trace")
    assert evidence_trace.status == VerificationStatus.passed


@pytest.mark.skipif(
    os.getenv("PIKO_ENABLE_REAL_CONNECTORS") != "true" or os.getenv("PIKO_LIVE_CONNECTOR_TEST") != "true",
    reason="Live source-to-evidence smoke requires explicit PIKO_ENABLE_REAL_CONNECTORS=true and PIKO_LIVE_CONNECTOR_TEST=true.",
)
def test_live_pcgamingwiki_source_to_evidence_chain() -> None:
    get_settings.cache_clear()
    report = run_article_pipeline(
        WorkflowStartRequest(
            game_id="game_live_hades",
            game_name="Hades",
            topic="Where is the save file location?",
        )
    )

    assert report.agent_outputs["source_agent"]["real_collection_performed"] is True
    assert report.agent_outputs["evidence_agent"]["real_source_records_used"] is True
    assert report.pipeline_state.evidence_cards
    assert report.publish_decision is not None
    assert report.publish_decision.value == PublishDecisionValue.needs_more_evidence
    assert all(card.source_id in {source.source_id for source in report.pipeline_state.sources} for card in report.pipeline_state.evidence_cards)


def _run_mocked_real_source_workflow(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "true")
    monkeypatch.setenv("PIKO_LIVE_CONNECTOR_TEST", "true")
    get_settings.cache_clear()

    records = [
        ConnectorSearchResult.model_validate(record)
        for record in _pilot_1_records()
        if record["title"] == "Hades"
    ]

    def fake_search(self, query: str, limit: int = 3):
        assert query == "Hades"
        assert limit <= 3
        return records

    monkeypatch.setattr("packages.collectors.pcgamingwiki.PCGamingWikiConnector.search", fake_search)
    try:
        return run_article_pipeline(
            WorkflowStartRequest(
                game_id="game_fixture_hades",
                game_name="Hades",
                topic="Where is the save file location?",
            )
        )
    finally:
        monkeypatch.delenv("PIKO_ENABLE_REAL_CONNECTORS", raising=False)
        monkeypatch.delenv("PIKO_LIVE_CONNECTOR_TEST", raising=False)
        get_settings.cache_clear()
