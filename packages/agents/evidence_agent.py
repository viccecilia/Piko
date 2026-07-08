from packages.agents.base import BaseAgent
from packages.collectors.local_fixtures import get_fixtures_by_ids, select_local_source_candidates
from packages.indexing.evidence_extractor import extract_evidence_cards_from_fixtures, extract_evidence_cards_from_source_records
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class EvidenceAgent(BaseAgent):
    definition = AgentDefinition(
        name="evidence_agent",
        label="Evidence Agent",
        purpose="Extract mock evidence cards and claim candidates from selected sources.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        source_records = request.payload.get("source_records") if request.payload else None
        if source_records:
            evidence_cards = extract_evidence_cards_from_source_records(source_records)
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "evidence_cards": evidence_cards,
                    "claim_candidates": evidence_cards,
                    "evidence_status": "needs_more_evidence",
                    "real_source_records_used": True,
                },
                source_ids=sorted({str(card["source_id"]) for card in evidence_cards}),
            )

        source_ids = request.payload.get("source_ids") if request.payload else None
        if not source_ids:
            source_ids = [
                source["source_id"]
                for source in select_local_source_candidates(request.game_name, request.topic)[:4]
            ]
        evidence_cards = extract_evidence_cards_from_fixtures(get_fixtures_by_ids(source_ids))
        if not evidence_cards:
            evidence_cards = [
                {
                    "evidence_card_id": "ev_mock_001",
                    "source_id": "source_mock_official",
                    "claim_type": "solution",
                    "symptom": request.topic,
                    "solution": "Verify game files",
                    "platform": "windows",
                    "confidence": 82,
                },
                {
                    "evidence_card_id": "ev_mock_002",
                    "source_id": "source_mock_discussion",
                    "claim_type": "solution",
                    "symptom": request.topic,
                    "solution": "Disable Steam Overlay",
                    "platform": "windows",
                    "confidence": 74,
                },
            ]
        return AgentRunResponse(
            agent=self.definition.name,
            output={"evidence_cards": evidence_cards, "claim_candidates": evidence_cards},
            source_ids=sorted({str(card["source_id"]) for card in evidence_cards}),
        )
