import os
import json
from pathlib import Path

import pytest

from packages.indexing.evidence_extractor import extract_evidence_cards_from_source_records
from packages.agents.registry import agent_registry
from packages.shared.schemas import AgentRunRequest
from packages.shared.config import get_settings
from packages.agents.writer_agent import WriterAgent
from packages.workflows.content_benchmark import build_article_from_source_records, build_comparison_report


STARDew_SOURCE_RECORD = {
    "source_id": "pcgamingwiki_31535",
    "source_type": "pcgamingwiki",
    "url": "https://www.pcgamingwiki.com/w/api.php?curid=31535",
    "title": "Stardew Valley",
    "retrieved_at": "2026-06-21T07:11:10.209049Z",
    "trust_tier": "reference",
    "snippet": "===Save game data location===\n{{Game data|\n{{Game data/saves|Windows|{{p|appdata}}\\StardewValley\\Saves\\}}\n{{Game data/saves|OS X|{{p|osxhome}}/.config/StardewValley/Saves/}}\n{{Game data/saves|Linux|{{p|xdgconfighome}}/StardewValley/Saves/}}\n}}",
    "clean_text": "===Save game data location===\n{{Game data|\n{{Game data/saves|Windows|{{p|appdata}}\\StardewValley\\Saves\\}}\n{{Game data/saves|OS X|{{p|osxhome}}/.config/StardewValley/Saves/}}\n{{Game data/saves|Linux|{{p|xdgconfighome}}/StardewValley/Saves/}}\n}}",
    "raw_text": None,
    "metadata": {"pageid": "31535", "section": "Save game data location", "raw_text_included": False},
}


def test_stardew_source_record_generates_save_location_evidence() -> None:
    cards = extract_evidence_cards_from_source_records([STARDew_SOURCE_RECORD])

    save_cards = [card for card in cards if card["claim_type"] == "save_location"]
    assert len(save_cards) == 3
    assert {card["platform"] for card in save_cards} == {"windows", "mac", "linux"}
    assert all(card["source_id"] == "pcgamingwiki_31535" for card in save_cards)
    assert all(card["url"] for card in save_cards)
    assert all(card["retrieved_at"] for card in save_cards)


def test_content_benchmark_article_is_source_traced_and_not_publish_ready() -> None:
    article = build_article_from_source_records([STARDew_SOURCE_RECORD])

    assert article["publish_ready"] is False
    assert article["publishing_performed"] is False
    assert article["real_collection_performed"] is False
    assert article["llm_used"] is False
    assert article["source_trace_present"] is True
    assert article["evidence_trace_present"] is True
    assert article["agent_path"] == [
        "source_agent",
        "evidence_agent",
        "ranking_agent",
        "writer_agent",
        "editor_agent",
        "factcheck_agent",
    ]
    assert article["status"] == "draft_benchmark_only"
    assert [step["agent"] for step in article["agent_trace"]] == [
        "source_agent",
        "evidence_agent",
        "ranking_agent",
        "writer_agent",
        "editor_agent",
        "factcheck_agent",
    ]
    assert len(article["platform_locations"]) == 3
    assert article["evidence_to_claim_trace"]
    assert article["writer_output"]["game"] == "Stardew Valley"
    assert article["writer_output"]["publish_ready"] is False
    assert article["writer_output"]["publishing_performed"] is False
    assert article["writer_output"]["llm_used"] is False
    assert "Example Game" not in article["markdown"]
    assert "Do not download unknown" in article["markdown"]
    assert "pcgamingwiki_31535" in {trace["source_id"] for trace in article["evidence_to_claim_trace"]}
    assert article["verification_report"]["status"] == "pass"


def test_writer_agent_consumes_real_evidence_and_ranked_steps() -> None:
    article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    writer_output = article["writer_output"]

    assert writer_output["game"] == "Stardew Valley"
    assert writer_output["source_ids"] == ["pcgamingwiki_31535"]
    assert writer_output["used_source_ids"] == writer_output["source_ids"]
    assert any(card_id.endswith("_save_windows") for card_id in writer_output["evidence_card_ids"])
    assert "Stardew Valley Save File Location" in writer_output["markdown"]
    assert "Example Game Crash on Startup Fix" not in writer_output["markdown"]


def test_source_evidence_rank_writer_artifact_trace_is_complete() -> None:
    article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    source_ids = {source["source_id"] for source in article["sources"]}
    evidence_source_ids = {card["source_id"] for card in article["evidence_cards"]}
    ranked_source_ids = {source_id for step in article["ranked_steps"] for source_id in step["source_ids"]}
    writer_source_ids = set(article["writer_output"]["source_ids"])

    assert source_ids == {"pcgamingwiki_31535"}
    assert evidence_source_ids == source_ids
    assert ranked_source_ids == source_ids
    assert writer_source_ids == source_ids
    assert all(trace["source_id"] in source_ids for trace in article["evidence_to_claim_trace"])


def test_writer_agent_without_real_payload_keeps_legacy_mock_behavior() -> None:
    output = WriterAgent().run(AgentRunRequest()).output

    assert "Example Game Crash on Startup Fix" in output["draft_excerpt"]
    assert output["llm_used"] is False
    assert output["used_source_ids"] == output["source_ids"]


class MockLLMWriterAdapter:
    def generate(self, payload):
        first_claim = payload["evidence_cards"][0]["claim"]
        source_ids = sorted({card["source_id"] for card in payload["evidence_cards"]})
        return {
            "markdown": (
                "# Stardew Valley Save File Location\n\n"
                f"{first_claim}\n\n"
                "Back up the save folder before editing or moving files.\n"
            ),
            "claim_trace": [
                {
                    "claim": card["claim"],
                    "source_id": card["source_id"],
                    "evidence_card_id": card["evidence_card_id"],
                    "confidence": card["confidence"],
                }
                for card in payload["evidence_cards"]
            ],
            "used_source_ids": source_ids,
            "uncertainty_notes": ["Mock LLM output remains draft-only."],
            "risk_notes": ["Back up saves first."],
            "publish_ready": False,
            "publishing_performed": False,
            "model": "mock-llm-writer",
        }


class SourceIdsOnlyLLMWriterAdapter:
    def generate(self, payload):
        first_claim = payload["evidence_cards"][0]["claim"]
        source_ids = sorted({card["source_id"] for card in payload["evidence_cards"]})
        return {
            "markdown": f"# Stardew Valley Save File Location\n\n{first_claim}\n",
            "claim_trace": [
                {
                    "claim": card["claim"],
                    "source_id": card["source_id"],
                    "evidence_card_id": card["evidence_card_id"],
                    "confidence": card["confidence"],
                }
                for card in payload["evidence_cards"]
            ],
            "source_ids": source_ids,
            "uncertainty_notes": ["Mock LLM output remains draft-only."],
            "risk_notes": ["Back up saves first."],
            "publish_ready": False,
            "publishing_performed": False,
            "model": "mock-source-ids-only-llm",
        }


class UnsupportedTraceLLMWriterAdapter:
    def generate(self, payload):
        first_claim = payload["evidence_cards"][0]["claim"]
        return {
            "markdown": f"# Stardew Valley Save File Location\n\n{first_claim}\n",
            "claim_trace": [
                {
                    "claim": "Unsupported claim from mock LLM",
                    "source_id": "missing_source",
                    "evidence_card_id": "missing_card",
                    "confidence": 99,
                }
            ],
            "used_source_ids": ["missing_source"],
            "uncertainty_notes": ["This should fail trace verification."],
            "risk_notes": ["Back up saves first."],
            "publish_ready": False,
            "publishing_performed": False,
            "model": "mock-unsupported-llm",
        }


def test_llm_writer_disabled_by_default_uses_rule_based_path() -> None:
    get_settings.cache_clear()
    output = WriterAgent(llm_adapter=MockLLMWriterAdapter()).run(
        AgentRunRequest(
            game_id="game_stardew_valley",
            game_name="Stardew Valley",
            topic="save file location",
            payload={
                "evidence_cards": extract_evidence_cards_from_source_records([STARDew_SOURCE_RECORD]),
                "ranked_steps": [
                    {
                        "rank": 1,
                        "solution": "Check the platform-specific save folder first.",
                        "confidence": 78,
                        "risk_level": "low",
                        "source_ids": ["pcgamingwiki_31535"],
                    }
                ],
                "sources": [STARDew_SOURCE_RECORD],
            },
        )
    ).output

    assert output["llm_used"] is False
    assert output["source_ids"] == ["pcgamingwiki_31535"]
    assert output["used_source_ids"] == output["source_ids"]
    assert output["publish_ready"] is False
    assert output["publishing_performed"] is False
    assert "Stardew Valley Save File Location" in output["markdown"]


def test_mock_llm_writer_output_goes_through_artifact_factcheck_and_verification(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "true")
    get_settings.cache_clear()
    writer = agent_registry._agents["writer_agent"]
    original_adapter = writer.llm_adapter
    writer.llm_adapter = MockLLMWriterAdapter()
    try:
        article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    finally:
        writer.llm_adapter = original_adapter
        monkeypatch.delenv("PIKO_ENABLE_LLM_WRITER", raising=False)
        get_settings.cache_clear()

    assert article["llm_used"] is True
    assert article["writer_output"]["llm_used"] is True
    assert article["writer_output"]["llm_model"] == "mock-llm-writer"
    assert article["writer_output"]["source_ids"] == ["pcgamingwiki_31535"]
    assert article["writer_output"]["used_source_ids"] == article["writer_output"]["source_ids"]
    assert article["publish_ready"] is False
    assert article["publishing_performed"] is False
    assert article["factcheck_output"]["factcheck_pass"] is True
    assert article["verification_report"]["status"] == "pass"


def test_mock_llm_source_ids_alias_is_preserved_when_source_ids_field_is_returned(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "true")
    get_settings.cache_clear()
    writer = agent_registry._agents["writer_agent"]
    original_adapter = writer.llm_adapter
    writer.llm_adapter = SourceIdsOnlyLLMWriterAdapter()
    try:
        article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    finally:
        writer.llm_adapter = original_adapter
        monkeypatch.delenv("PIKO_ENABLE_LLM_WRITER", raising=False)
        get_settings.cache_clear()

    writer_output = article["writer_output"]
    assert writer_output["llm_used"] is True
    assert writer_output["llm_model"] == "mock-source-ids-only-llm"
    assert writer_output["source_ids"] == ["pcgamingwiki_31535"]
    assert writer_output["used_source_ids"] == writer_output["source_ids"]
    assert writer_output["publish_ready"] is False
    assert writer_output["publishing_performed"] is False


def test_unsupported_llm_claim_trace_is_caught_by_factcheck_and_verification(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "true")
    get_settings.cache_clear()
    writer = agent_registry._agents["writer_agent"]
    original_adapter = writer.llm_adapter
    writer.llm_adapter = UnsupportedTraceLLMWriterAdapter()
    try:
        article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    finally:
        writer.llm_adapter = original_adapter
        monkeypatch.delenv("PIKO_ENABLE_LLM_WRITER", raising=False)
        get_settings.cache_clear()

    assert article["llm_used"] is True
    assert article["factcheck_output"]["factcheck_pass"] is False
    assert article["factcheck_output"]["missing_source_ids"] == ["missing_source"]
    assert article["factcheck_output"]["missing_evidence_card_ids"] == ["missing_card"]
    assert article["verification_report"]["status"] == "fail"


@pytest.mark.skipif(
    os.getenv("PIKO_ENABLE_LLM_WRITER") != "true" or os.getenv("PIKO_LIVE_LLM_TEST") != "true",
    reason="Live LLM writer smoke requires explicit PIKO_ENABLE_LLM_WRITER=true and PIKO_LIVE_LLM_TEST=true.",
)
def test_live_llm_writer_smoke_requires_key_and_stays_draft_only() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY is not set; live LLM smoke skipped.")
    get_settings.cache_clear()
    article = build_article_from_source_records([STARDew_SOURCE_RECORD])

    assert article["llm_used"] is True
    assert article["publish_ready"] is False
    assert article["publishing_performed"] is False
    assert article["verification_report"]["status"] in {"pass", "fail"}


def test_content_comparison_report_is_structured() -> None:
    article = build_article_from_source_records([STARDew_SOURCE_RECORD])
    report = build_comparison_report(
        article,
        [
            {
                "title": "PCGamingWiki Stardew Valley",
                "url": "https://www.pcgamingwiki.com/wiki/Stardew_Valley",
                "source_type": "reference_wiki",
                "covers": "Structured save-location data.",
                "notes": "Useful source; less direct as a player checklist.",
            }
        ],
    )

    assert report["materials"]
    assert "Piko's draft is clearer" in report["markdown"]
    assert report["next_recommendation"]


def test_article_draft_artifacts_preserve_writer_source_id_alias_contract() -> None:
    artifact_paths = sorted(Path("artifacts/article_drafts").glob("*.json"))
    assert artifact_paths
    for path in artifact_paths:
        artifact = json.loads(path.read_text(encoding="utf-8"))
        writer_output = artifact.get("writer_output") or {}
        if "source_ids" in writer_output or "used_source_ids" in writer_output:
            assert writer_output.get("source_ids") is not None, f"{path} missing writer_output.source_ids"
            assert writer_output.get("used_source_ids") is not None, f"{path} missing writer_output.used_source_ids"
            assert writer_output["source_ids"] == writer_output["used_source_ids"], path
        assert artifact.get("publish_ready") is False, path
        assert artifact.get("publishing_performed") is False, path
        if writer_output.get("llm_fallback_used") is True:
            assert writer_output["source_ids"] == writer_output["used_source_ids"], path
            assert writer_output.get("publishing_performed") is False, path
            assert writer_output.get("publish_ready") is False, path
