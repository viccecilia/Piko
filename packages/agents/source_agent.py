from packages.agents.base import BaseAgent
from packages.collectors.local_fixtures import select_local_source_candidates
from packages.collectors.pcgamingwiki import PCGamingWikiConnector
from packages.shared.config import get_settings
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class SourceAgent(BaseAgent):
    definition = AgentDefinition(
        name="source_agent",
        label="Source Agent",
        purpose="Select source types and mock source IDs for one player need.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        provided_source_records = request.payload.get("source_records") if request.payload else None
        if provided_source_records:
            sources = [
                {
                    **source,
                    "priority": index,
                    "provided_source_record": True,
                }
                for index, source in enumerate(provided_source_records, start=1)
            ]
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "sources": sources,
                    "real_collection_performed": False,
                    "provided_source_records_used": True,
                    "fixture_selection": False,
                    "connector": "provided_pcgamingwiki_mediawiki_record",
                    "query": request.game_name,
                },
                source_ids=[source["source_id"] for source in sources],
            )

        settings = get_settings()
        if settings.enable_real_connectors and settings.live_connector_test:
            results = PCGamingWikiConnector().search(request.game_name, limit=3)
            sources = [
                {
                    **result.model_dump(mode="json"),
                    "priority": index,
                    "real_source_candidate": True,
                }
                for index, result in enumerate(results, start=1)
            ]
            return AgentRunResponse(
                agent=self.definition.name,
                output={
                    "sources": sources,
                    "real_collection_performed": True,
                    "fixture_selection": False,
                    "connector": "pcgamingwiki_mediawiki",
                    "query": request.game_name,
                },
                source_ids=[source["source_id"] for source in sources],
            )

        fixture_candidates = select_local_source_candidates(request.game_name, request.topic)
        sources = [
            {
                **candidate,
                "priority": index,
            }
            for index, candidate in enumerate(fixture_candidates[:4], start=1)
        ]
        if not sources:
            sources = [
                {"source_id": "source_mock_official", "source_type": "official_notes", "priority": 1},
                {"source_id": "source_mock_wiki", "source_type": "pcgamingwiki", "priority": 2},
                {"source_id": "source_mock_discussion", "source_type": "steam_discussion", "priority": 3},
                {"source_id": "source_mock_forum", "source_type": "community_forum", "priority": 4},
            ]
        return AgentRunResponse(
            agent=self.definition.name,
            output={"sources": sources, "real_collection_performed": False, "fixture_selection": bool(fixture_candidates)},
            source_ids=[source["source_id"] for source in sources],
        )
