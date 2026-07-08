from packages.agents.evidence_agent import EvidenceAgent
from packages.agents.source_agent import SourceAgent
from packages.collectors.local_fixtures import load_local_source_fixtures, select_local_source_candidates
from packages.indexing.claim_trace import verify_draft_claim_trace
from packages.indexing.evidence_extractor import extract_evidence_cards_from_fixtures
from packages.shared.schemas import AgentRunRequest, DraftArtifact, EvidenceCard, WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline


def test_local_source_fixtures_load_and_validate() -> None:
    fixtures = load_local_source_fixtures()

    assert len(fixtures) >= 4
    assert {fixture.source_type for fixture in fixtures} >= {"official_notes", "pcgamingwiki", "steam_discussion", "protondb"}
    assert all(fixture.url.startswith("https://example.invalid/") for fixture in fixtures)
    assert all(len(fixture.content) < 1200 for fixture in fixtures)


def test_source_agent_selects_local_fixture_candidates() -> None:
    response = SourceAgent().run(
        AgentRunRequest(game_name="Example Game", topic="black screen crash on startup")
    )

    assert response.output["real_collection_performed"] is False
    assert response.output["fixture_selection"] is True
    assert response.output["sources"][0]["source_id"].startswith("fixture_")
    assert response.output["sources"][0]["reason"]


def test_source_candidate_selection_no_match_returns_empty() -> None:
    candidates = select_local_source_candidates("Unknown Game", "unrelated fishing puzzle")

    assert candidates == []


def test_evidence_extraction_references_valid_source_ids() -> None:
    fixtures = load_local_source_fixtures()
    cards = extract_evidence_cards_from_fixtures(fixtures)
    fixture_ids = {fixture.source_id for fixture in fixtures}

    assert cards
    assert {str(card["source_id"]) for card in cards}.issubset(fixture_ids)
    assert all(card["evidence_card_id"] for card in cards)
    assert all(card["quote_snippet"] for card in cards)


def test_evidence_agent_extracts_cards_from_local_fixtures() -> None:
    response = EvidenceAgent().run(
        AgentRunRequest(game_name="Example Game", topic="black screen crash on startup")
    )

    cards = response.output["evidence_cards"]
    assert cards
    assert all(card["source_id"].startswith("fixture_") for card in cards)


def test_claim_trace_maps_draft_to_evidence() -> None:
    card = EvidenceCard(
        evidence_card_id="ev_fixture_001",
        source_id="fixture_official_launch_001",
        claim_type="solution",
        claim="Verify game files",
        solution="Verify game files",
        confidence=82,
    )
    trace = verify_draft_claim_trace(
        DraftArtifact(body="Start by using Verify game files before risky fixes."),
        [card],
    )

    assert trace["passed"] is True
    assert trace["supported_claims"][0]["source_id"] == "fixture_official_launch_001"


def test_workflow_uses_local_fixture_evidence() -> None:
    result = run_article_pipeline(
        WorkflowStartRequest(game_name="Example Game", topic="black screen crash on startup")
    )

    source_ids = {source.source_id for source in result.pipeline_state.sources}
    evidence_source_ids = {card.source_id for card in result.pipeline_state.evidence_cards}
    assert source_ids
    assert evidence_source_ids.issubset(source_ids)
    assert result.pipeline_state.publish_decision is not None
