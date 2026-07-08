import json
import re
from pathlib import Path
from typing import Any

from packages.agents.registry import agent_registry
from packages.indexing.evidence_extractor import extract_evidence_cards_from_source_records
from packages.shared.schemas import AgentRunRequest


ARTICLE_SLUG = "stardew-valley-save-file-location"


def build_article_from_source_records(source_records: list[dict[str, Any]]) -> dict[str, Any]:
    return run_content_benchmark_agent_workflow(source_records)["article"]


def run_content_benchmark_agent_workflow(source_records: list[dict[str, Any]]) -> dict[str, Any]:
    request = AgentRunRequest(
        game_id="game_stardew_valley",
        game_name="Stardew Valley",
        topic="save file location and what to check first if saves do not appear",
        payload={"source_records": source_records},
    )
    source_response = agent_registry.run("source_agent", request)
    sources = source_response.output["sources"]

    evidence_response = agent_registry.run(
        "evidence_agent",
        AgentRunRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.topic,
            payload={"source_records": sources},
        ),
    )
    evidence_cards = evidence_response.output["evidence_cards"]

    ranking_response = agent_registry.run(
        "ranking_agent",
        AgentRunRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.topic,
            payload={"evidence_cards": evidence_cards},
        ),
    )
    ranked_steps = ranking_response.output["ranked_solutions"]

    writer_response = agent_registry.run(
        "writer_agent",
        AgentRunRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.topic,
            payload={"sources": sources, "evidence_cards": evidence_cards, "ranked_steps": ranked_steps},
        ),
    )
    editor_response = agent_registry.run(
        "editor_agent",
        AgentRunRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.topic,
            payload={"draft": writer_response.output["markdown"]},
        ),
    )
    final_markdown = editor_response.output.get("edited_text") or writer_response.output["markdown"]
    factcheck_response = agent_registry.run(
        "factcheck_agent",
        AgentRunRequest(
            game_id=request.game_id,
            game_name=request.game_name,
            topic=request.topic,
            payload={"draft": final_markdown, "evidence_cards": evidence_cards, "writer_output": writer_response.output},
        ),
    )

    save_cards = [card for card in evidence_cards if card.get("claim_type") == "save_location"]
    source_summary = [
        {
            "source_id": source["source_id"],
            "source_type": source.get("source_type"),
            "title": source.get("title"),
            "url": source.get("url"),
            "retrieved_at": source.get("retrieved_at"),
            "trust_tier": source.get("trust_tier"),
        }
        for source in sources
    ]
    agent_trace = [
        {"agent": "source_agent", "source_ids": source_response.source_ids, "output_keys": sorted(source_response.output.keys())},
        {"agent": "evidence_agent", "source_ids": evidence_response.source_ids, "output_keys": sorted(evidence_response.output.keys())},
        {"agent": "ranking_agent", "source_ids": ranking_response.source_ids, "output_keys": sorted(ranking_response.output.keys())},
        {"agent": "writer_agent", "source_ids": writer_response.source_ids, "output_keys": sorted(writer_response.output.keys())},
        {"agent": "editor_agent", "source_ids": editor_response.source_ids, "output_keys": sorted(editor_response.output.keys())},
        {"agent": "factcheck_agent", "source_ids": factcheck_response.source_ids, "output_keys": sorted(factcheck_response.output.keys())},
    ]
    agent_path = [step["agent"] for step in agent_trace]
    source_ids = {source["source_id"] for source in source_summary}
    evidence_source_ids = {card["source_id"] for card in evidence_cards if card.get("source_id")}
    trace_card_ids = {trace["evidence_card_id"] for trace in writer_response.output["claim_trace"] if trace.get("evidence_card_id")}
    evidence_card_ids = {card["evidence_card_id"] for card in evidence_cards if card.get("evidence_card_id")}
    source_trace_present = bool(source_ids) and evidence_source_ids.issubset(source_ids)
    evidence_trace_present = bool(trace_card_ids) and trace_card_ids.issubset(evidence_card_ids)
    factcheck_pass = bool(factcheck_response.output.get("factcheck_pass"))
    verification_report = {
        "status": "pass" if source_trace_present and evidence_trace_present and factcheck_pass else "fail",
        "checks": [
            {"name": "source_trace_present", "passed": source_trace_present},
            {"name": "evidence_trace_present", "passed": evidence_trace_present},
            {"name": "factcheck_pass", "passed": factcheck_pass},
            {"name": "no_publishing_side_effect", "passed": not bool(writer_response.output.get("publishing_performed"))},
        ],
        "summary": "Benchmark artifact verification mirrors source, evidence, factcheck, and publishing safety checks.",
    }
    article = {
        "slug": ARTICLE_SLUG,
        "game": "Stardew Valley",
        "player_question": "Stardew Valley save file location and what to check first if saves do not appear",
        "intent": "Help players quickly find Stardew Valley save folders and avoid risky save-file troubleshooting.",
        "status": "draft_benchmark_only",
        "publish_ready": False,
        "publishing_performed": bool(writer_response.output.get("publishing_performed")),
        "real_collection_performed": bool(source_response.output.get("real_collection_performed")),
        "llm_used": bool(writer_response.output.get("llm_used")),
        "llm_fallback_used": bool(writer_response.output.get("llm_fallback_used")),
        "llm_error": writer_response.output.get("llm_error"),
        "agent_path": agent_path,
        "source_trace_present": source_trace_present,
        "evidence_trace_present": evidence_trace_present,
        "quick_answer": _quick_answer(save_cards),
        "platform_locations": _platform_locations(save_cards),
        "ranked_steps": ranked_steps,
        "writer_output": writer_response.output,
        "editor_output": editor_response.output,
        "factcheck_output": factcheck_response.output,
        "verification_report": verification_report,
        "agent_trace": agent_trace,
        "risk_notes": [
            "Back up the entire save folder before moving, deleting, editing, or replacing files.",
            "Do not download unknown save editors, DLL files, or patches just to recover a save.",
            "Cloud sync can overwrite local changes; copy saves elsewhere before testing sync fixes.",
        ],
        "uncertainty_notes": [
            "This benchmark draft uses a controlled PCGamingWiki/MediaWiki source sample plus a small manual comparison set.",
            "It should stay a draft until a future round verifies page-level evidence and platform-specific edge cases.",
        ],
        "sources": source_summary,
        "evidence_cards": evidence_cards,
        "evidence_to_claim_trace": writer_response.output["claim_trace"],
    }
    article["markdown"] = final_markdown
    return {"article": article, "agent_outputs": {
        "source_agent": source_response.output,
        "evidence_agent": evidence_response.output,
        "ranking_agent": ranking_response.output,
        "writer_agent": writer_response.output,
        "editor_agent": editor_response.output,
        "factcheck_agent": factcheck_response.output,
    }}


def render_article_markdown(article: dict[str, Any]) -> str:
    lines = [
        "# Stardew Valley Save File Location",
        "",
        "If your Stardew Valley save is missing, do not reinstall or edit files first. Start by checking the save folder for your platform, then make a backup before trying anything else.",
        "",
        "## Quick Answer",
        article["quick_answer"],
        "",
        "## Save File Locations",
    ]
    for location in article["platform_locations"]:
        lines.append(f"- **{location['platform']}**: `{location['path']}`")
    lines.extend(
        [
            "",
            "## What To Check First",
            "1. Open the save folder for your platform and check whether your farm folder is still there.",
            "2. Copy the whole save folder somewhere safe before moving, deleting, or editing anything.",
            "3. If the game does not show the save, check whether cloud sync restored or replaced the local files.",
            "",
            "## Do Not Try First",
            "- Do not download unknown recovery tools, DLL files, or save patches.",
            "- Do not delete the original save folder without a backup.",
            "- Do not overwrite cloud and local saves until you know which one is newer.",
            "",
            "## Sources",
        ]
    )
    for source in article["sources"]:
        lines.append(f"- {source['title']} ({source['source_type']}): {source['url']}")
    lines.extend(
        [
            "",
            "## Confidence",
            "Draft benchmark only. Source trace is present, but this page should remain unpublished until a future verification round checks source freshness and platform edge cases.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_article_artifacts(article: dict[str, Any], directory: str = "artifacts/article_drafts") -> tuple[Path, Path]:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / f"{ARTICLE_SLUG}.json"
    md_path = target / f"{ARTICLE_SLUG}.md"
    json_payload = {key: value for key, value in article.items() if key != "markdown"}
    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(article["markdown"], encoding="utf-8")
    return json_path, md_path


def build_comparison_report(article: dict[str, Any], materials: list[dict[str, Any]]) -> dict[str, Any]:
    report = {
        "slug": ARTICLE_SLUG,
        "piko_article": {
            "title": "Stardew Valley Save File Location",
            "strengths": [
                "Starts with the answer.",
                "Keeps risky actions behind backup warnings.",
                "Links claims to source IDs.",
                "Separates platform paths from troubleshooting steps.",
            ],
            "limits": article["uncertainty_notes"],
        },
        "materials": materials,
        "comparison_dimensions": [
            "direct_answer",
            "low_risk_first_step",
            "source_traceability",
            "platform_scope",
            "risk_warning",
            "clarity_for_nontechnical_player",
            "requires_clicking_out",
            "piko_has_incremental_value",
        ],
        "takeaways": [
            "Piko's draft is strongest as a short answer and risk-filtered checklist.",
            "PCGamingWiki is strong on structured paths, but its raw page format is not always player-friendly.",
            "Official/community wiki material can add context, but Piko should avoid copying tables or long prose.",
            "Next round should verify save folder paths against at least one official/community-maintained source before publishing.",
        ],
        "next_recommendation": "Keep as draft benchmark and add page-level source verification before any publishing eligibility step.",
    }
    report["markdown"] = render_comparison_markdown(report)
    return report


def render_comparison_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Stardew Valley Save File Location - Comparison",
        "",
        "## Summary",
        "Piko's draft is clearer as a player-facing checklist, but it still needs one more source-verification round before publishing.",
        "",
        "## Materials Checked",
    ]
    for item in report["materials"]:
        lines.extend(
            [
                f"- **{item['title']}**",
                f"  - URL: {item['url']}",
                f"  - Source type: {item['source_type']}",
                f"  - What it covers: {item['covers']}",
                f"  - Notes: {item['notes']}",
            ]
        )
    lines.extend(["", "## Piko Difference"])
    for strength in report["piko_article"]["strengths"]:
        lines.append(f"- {strength}")
    lines.extend(["", "## Piko Limits"])
    for limit in report["piko_article"]["limits"]:
        lines.append(f"- {limit}")
    lines.extend(["", "## Next Recommendation", report["next_recommendation"], ""])
    return "\n".join(lines)


def write_comparison_artifacts(report: dict[str, Any], directory: str = "artifacts/comparisons") -> tuple[Path, Path]:
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    json_path = target / f"{ARTICLE_SLUG}_comparison.json"
    md_path = target / f"{ARTICLE_SLUG}_comparison.md"
    json_payload = {key: value for key, value in report.items() if key != "markdown"}
    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(report["markdown"], encoding="utf-8")
    return json_path, md_path


def _quick_answer(cards: list[dict[str, Any]]) -> str:
    locations = _platform_locations(cards)
    if not locations:
        return "Need more evidence before naming exact save folders."
    return "Check the platform-specific Saves folder first, then back it up before editing or moving any files."


def _platform_locations(cards: list[dict[str, Any]]) -> list[dict[str, str]]:
    locations = []
    for card in cards:
        match = re.search(r"stored at (.+) on (.+)\.", str(card.get("claim")))
        if not match:
            continue
        locations.append({"path": match.group(1), "platform": str(card.get("platform"))})
    return locations
