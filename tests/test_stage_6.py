from datetime import date

from packages.indexing.llama_index_builder import build_in_memory_evidence_index
from packages.indexing.retrieval import retrieve_evidence
from packages.memory.memory_store import InMemoryMemoryStore, MemoryRecord
from packages.shared.schemas import EvidenceCard
from packages.workflows.source_refresh_pipeline import SourceFreshness, evaluate_refresh_signals


def test_in_memory_evidence_index_retrieves_source_linked_cards() -> None:
    card = EvidenceCard(
        evidence_card_id="ev_1",
        source_id="source_1",
        claim_type="solution",
        claim="Verify game files",
        solution="Verify game files",
        confidence=82,
    )
    index = build_in_memory_evidence_index([card])

    results = retrieve_evidence(index, "verify files")
    assert results == [
        {
            "evidence_card_id": "ev_1",
            "source_id": "source_1",
            "claim": "Verify game files",
            "confidence": 82,
        }
    ]


def test_memory_store_upsert_and_lookup_structured_judgment() -> None:
    store = InMemoryMemoryStore()
    record = MemoryRecord(
        memory_type="solution",
        key="verify_files",
        game_id="game_mock_001",
        value={"solution": "Verify game files", "risk": "low"},
        source_ids=["source_1"],
        confidence=82,
    )

    store.upsert(record)
    found = store.lookup("solution", "verify_files", "game_mock_001")

    assert found is not None
    assert found.value["risk"] == "low"
    assert "raw_text" not in found.value


def test_refresh_signals_are_advisory_only() -> None:
    signals = evaluate_refresh_signals(
        [
            SourceFreshness(source_id="source_changed", last_seen=date(2026, 6, 1), current_seen=date(2026, 6, 2)),
            SourceFreshness(source_id="source_same", last_seen=date(2026, 6, 1), current_seen=date(2026, 6, 1)),
        ]
    )

    assert signals[0].needs_refresh is True
    assert signals[1].needs_refresh is False
    assert all("publish" not in signal.reason.lower() for signal in signals)
