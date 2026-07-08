from packages.agents.base import BaseAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class RankingAgent(BaseAgent):
    definition = AgentDefinition(
        name="ranking_agent",
        label="Ranking Agent",
        purpose="Rank solution candidates by confidence, risk, evidence strength, and usefulness.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        evidence_cards = request.payload.get("evidence_cards") if request.payload else None
        if evidence_cards and any(card.get("claim_type") == "save_location" for card in evidence_cards):
            save_cards = [card for card in evidence_cards if card.get("claim_type") == "save_location"]
            source_ids = sorted({str(card.get("source_id")) for card in save_cards if card.get("source_id")})
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "ranked_solutions": [
                        {
                            "rank": 1,
                            "solution": "Check the platform-specific save folder first.",
                            "confidence": 78,
                            "risk_level": "low",
                            "source_ids": source_ids,
                            "evidence_card_ids": [str(card.get("evidence_card_id")) for card in save_cards],
                        },
                        {
                            "rank": 2,
                            "solution": "Back up the whole Saves folder before moving, deleting, or editing files.",
                            "confidence": 70,
                            "risk_level": "low",
                            "source_ids": source_ids,
                            "evidence_card_ids": [str(card.get("evidence_card_id")) for card in save_cards],
                        },
                    ],
                    "evidence_status": "answer_level_evidence",
                    "uncertainty": "Needs one more source-verification pass before publishing.",
                },
                source_ids=source_ids,
            )

        if evidence_cards and not any(card.get("solution") for card in evidence_cards):
            source_ids = sorted({str(card.get("source_id")) for card in evidence_cards if card.get("source_id")})
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "ranked_solutions": [],
                    "evidence_status": "needs_more_evidence",
                    "source_ids": source_ids,
                    "reason": "Real source candidates are traceable, but no answer-level evidence was extracted yet.",
                },
                source_ids=source_ids,
            )

        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "ranked_solutions": [
                    {
                        "rank": 1,
                        "solution": "Verify game files",
                        "confidence": 82,
                        "risk_level": "low",
                        "source_ids": ["fixture_official_launch_001", "fixture_wiki_launch_001"],
                    },
                    {
                        "rank": 2,
                        "solution": "Disable Steam Overlay",
                        "confidence": 74,
                        "risk_level": "low",
                        "source_ids": ["fixture_community_overlay_001"],
                    },
                ]
            },
            source_ids=["fixture_official_launch_001", "fixture_wiki_launch_001", "fixture_community_overlay_001"],
        )
