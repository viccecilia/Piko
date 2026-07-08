from packages.agents.base import BaseAgent
from packages.shared.schemas import DraftArtifact, EvidenceCard
from packages.indexing.claim_trace import verify_draft_claim_trace
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class FactcheckAgent(BaseAgent):
    definition = AgentDefinition(
        name="factcheck_agent",
        label="Fact-check Agent",
        purpose="Placeholder for claim-to-source verification before publishing.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        draft_body = request.payload.get("draft", "") if request.payload else ""
        cards_payload = request.payload.get("evidence_cards", []) if request.payload else []
        writer_output = request.payload.get("writer_output", {}) if request.payload else {}
        if draft_body and cards_payload:
            evidence_source_ids = {str(card.get("source_id")) for card in cards_payload if card.get("source_id")}
            evidence_card_ids = {str(card.get("evidence_card_id")) for card in cards_payload if card.get("evidence_card_id")}
            claim_trace = writer_output.get("claim_trace") or request.payload.get("claim_trace", [])
            missing_trace_sources = sorted(
                {
                    str(trace.get("source_id"))
                    for trace in claim_trace
                    if trace.get("source_id") and str(trace.get("source_id")) not in evidence_source_ids
                }
            )
            missing_trace_cards = sorted(
                {
                    str(trace.get("evidence_card_id"))
                    for trace in claim_trace
                    if trace.get("evidence_card_id") and str(trace.get("evidence_card_id")) not in evidence_card_ids
                }
            )
            trace = verify_draft_claim_trace(
                DraftArtifact(body=draft_body),
                [EvidenceCard.model_validate(card) for card in cards_payload],
            )
            passed = trace["passed"] and not missing_trace_sources and not missing_trace_cards
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "checked_claims": len(trace["supported_claims"]),
                    "missing_source_ids": missing_trace_sources,
                    "missing_evidence_card_ids": missing_trace_cards,
                    "unsupported_claims": trace["unsupported_claims"],
                    "platform_mismatches": [],
                    "factcheck_pass": passed,
                    "trace": trace,
                },
            )
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "checked_claims": 2,
                "missing_source_ids": [],
                "platform_mismatches": [],
                "factcheck_pass": True,
            },
            source_ids=["source_mock_official", "source_mock_discussion"],
        )
