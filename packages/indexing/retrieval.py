from packages.indexing.llama_index_builder import InMemoryEvidenceIndex
from packages.shared.schemas import EvidenceCard


def retrieve_evidence(index: InMemoryEvidenceIndex, question: str, limit: int = 5) -> list[dict[str, object]]:
    cards: list[EvidenceCard] = index.search(question, limit=limit)
    return [
        {
            "evidence_card_id": card.evidence_card_id,
            "source_id": card.source_id,
            "claim": card.claim or card.solution,
            "confidence": card.confidence,
        }
        for card in cards
    ]
