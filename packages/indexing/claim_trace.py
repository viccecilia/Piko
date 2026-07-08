from packages.shared.schemas import DraftArtifact, EvidenceCard


def find_supported_claims(draft: DraftArtifact, evidence_cards: list[EvidenceCard]) -> list[dict[str, object]]:
    body = draft.body.lower()
    supported: list[dict[str, object]] = []
    for card in evidence_cards:
        claim_text = (card.claim or card.solution or "").lower()
        if claim_text and claim_text in body:
            supported.append(
                {
                    "claim": card.claim or card.solution,
                    "evidence_card_id": card.evidence_card_id,
                    "source_id": card.source_id,
                    "supported": True,
                }
            )
    return supported


def find_unsupported_claims(draft: DraftArtifact, evidence_cards: list[EvidenceCard]) -> list[str]:
    supported_claims = {str(item["claim"]).lower() for item in find_supported_claims(draft, evidence_cards)}
    expected_claims = {
        (card.claim or card.solution or "").lower()
        for card in evidence_cards
        if card.claim or card.solution
    }
    body = draft.body.lower()
    return sorted(claim for claim in expected_claims if claim in body and claim not in supported_claims)


def verify_draft_claim_trace(draft: DraftArtifact, evidence_cards: list[EvidenceCard]) -> dict[str, object]:
    supported = find_supported_claims(draft, evidence_cards)
    unsupported = find_unsupported_claims(draft, evidence_cards)
    return {
        "supported_claims": supported,
        "unsupported_claims": unsupported,
        "passed": bool(supported) and not unsupported,
    }

