from packages.shared.schemas import EvidenceCard


class InMemoryEvidenceIndex:
    def __init__(self, cards: list[EvidenceCard] | None = None) -> None:
        self.cards = cards or []

    def add(self, card: EvidenceCard) -> None:
        self.cards.append(card)

    def search(self, query: str, limit: int = 5) -> list[EvidenceCard]:
        terms = [term for term in query.lower().split() if len(term) > 2]
        scored: list[tuple[int, EvidenceCard]] = []
        for card in self.cards:
            text = f"{card.claim or ''} {card.symptom or ''} {card.solution or ''} {card.platform or ''}".lower()
            score = sum(1 for term in terms if term in text)
            if score > 0:
                scored.append((score, card))
        return [card for _, card in sorted(scored, key=lambda item: -item[0])[:limit]]


def build_in_memory_evidence_index(cards: list[EvidenceCard]) -> InMemoryEvidenceIndex:
    return InMemoryEvidenceIndex(cards=list(cards))
