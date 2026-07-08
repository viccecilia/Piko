from packages.agents.base import BaseAgent
from packages.agents.adapters.llm_writer_adapter import LLMWriterAdapter, OpenAILLMWriterAdapter, build_llm_writer_payload
from packages.shared.config import get_settings
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


class WriterAgent(BaseAgent):
    definition = AgentDefinition(
        name="writer_agent",
        label="Writer Agent",
        purpose="Draft a source-based page from an article brief only.",
    )

    def __init__(self, llm_adapter: LLMWriterAdapter | None = None) -> None:
        self.llm_adapter = llm_adapter

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        payload = request.payload or {}
        evidence_cards = payload.get("evidence_cards") or []
        ranked_steps = payload.get("ranked_steps") or []
        sources = payload.get("sources") or []
        if evidence_cards and ranked_steps:
            return self._run_source_backed_writer(request, evidence_cards, ranked_steps, sources)

        steps = [
            {
                "heading": "Verify game files",
                "body": "Use this first because it is low risk and source-backed.",
                "risk": "Low",
                "source_ids": ["fixture_official_launch_001", "fixture_wiki_launch_001"],
            },
            {
                "heading": "Disable Steam Overlay",
                "body": "Try this if the black screen appears after clicking Play.",
                "risk": "Low",
                "source_ids": ["fixture_community_overlay_001"],
            },
        ]
        source_ids = sorted({source_id for step in steps for source_id in step["source_ids"]})
        draft = "\n".join(
            [
                "# Example Game Crash on Startup Fix",
                "",
                "## Short Answer",
                "Start with low-risk fixes: verify game files, then disable Steam Overlay.",
                "",
                "## Steps",
                *[
                    f"### {index}. {step['heading']}\n{step['body']}\nRisk: {step['risk']}.\nSources: {', '.join(step['source_ids'])}"
                    for index, step in enumerate(steps, start=1)
                ],
                "",
                "## Risk Notes",
                "Do not download unknown DLL files, replace executables, or delete saves without a backup.",
                "",
                "## If It Fails",
                "Separate Windows fixes from Steam Deck / Proton notes before trying platform-specific steps.",
                "",
                "## Sources",
                "- fixture_official_launch_001",
                "- fixture_wiki_launch_001",
                "- fixture_community_overlay_001",
            ]
        )
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "draft_format": "markdown",
                "draft_excerpt": draft,
                "sections": ["short_answer", "steps", "risk_notes", "if_it_fails", "sources"],
                "source_ids": source_ids,
                "used_source_ids": source_ids,
                "used_raw_sources": False,
                "publishing_performed": False,
                "publish_ready": False,
                "llm_used": False,
                "llm_fallback_used": False,
            },
        )

    def _run_source_backed_writer(
        self,
        request: AgentRunRequest,
        evidence_cards: list[dict],
        ranked_steps: list[dict],
        sources: list[dict],
    ) -> AgentRunResponse:
        llm_response = self._maybe_run_llm_writer(request, evidence_cards, ranked_steps)
        llm_error = None
        if llm_response:
            if llm_response.get("ok"):
                try:
                    return self._response_from_llm_output(request, evidence_cards, ranked_steps, llm_response["output"])
                except Exception as exc:
                    llm_error = str(exc)
            else:
                llm_error = llm_response.get("error")

        save_cards = [card for card in evidence_cards if card.get("claim_type") == "save_location"]
        if not save_cards:
            return self._run_troubleshooting_writer(request, evidence_cards, ranked_steps, sources, llm_error)

        locations = [
            {
                "platform": card.get("platform"),
                "path": str(card.get("solution", "")).replace("Check ", ""),
                "source_id": card.get("source_id"),
                "evidence_card_id": card.get("evidence_card_id"),
            }
            for card in save_cards
        ]
        source_ids = sorted({str(card.get("source_id")) for card in evidence_cards if card.get("source_id")})
        evidence_card_ids = [str(card.get("evidence_card_id")) for card in evidence_cards if card.get("evidence_card_id")]
        claim_trace = [
            {
                "claim": card.get("claim"),
                "source_id": card.get("source_id"),
                "evidence_card_id": card.get("evidence_card_id"),
                "confidence": card.get("confidence"),
            }
            for card in evidence_cards
        ]
        title = f"{request.game_name} Save File Location"
        lines = [
            f"# {title}",
            "",
            f"If your {request.game_name} save is missing, do not reinstall or edit files first. Check the save folder for your platform, then make a backup before changing anything.",
            "",
            "## Quick Answer",
            "Check the platform-specific Saves folder first, then back it up before editing or moving any files.",
            "",
            "## Save File Locations",
        ]
        for location in locations:
            matching_card = next((card for card in evidence_cards if card.get("evidence_card_id") == location["evidence_card_id"]), {})
            claim = matching_card.get("claim") or f"{request.game_name} save files are stored at {location['path']} on {location['platform']}."
            lines.append(f"- **{location['platform']}**: `{location['path']}`. {claim}")
        lines.extend(
            [
                "",
                "## What To Check First",
                *[
                    f"{step['rank']}. {step['solution']}\nSources: {', '.join(step['source_ids'])}"
                    for step in ranked_steps
                ],
                "",
                "## Do Not Try First",
                "- Do not download unknown recovery tools, DLL files, or save patches.",
                "- Do not delete the original save folder without a backup.",
                "- Do not overwrite cloud and local saves until you know which one is newer.",
                "",
                "## Sources",
            ]
        )
        for source in sources:
            lines.append(f"- {source.get('title')} ({source.get('source_type')}): {source.get('url')}")
        lines.extend(
            [
                "",
                "## Confidence",
                "Draft benchmark only. Source trace is present, but this page should remain unpublished until a future verification round checks source freshness and platform edge cases.",
            ]
        )
        draft = "\n".join(lines) + "\n"
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "game": request.game_name,
                "player_question": request.topic,
                "draft_format": "markdown",
                "draft_excerpt": draft,
                "markdown": draft,
                "sections": ["quick_answer", "save_file_locations", "what_to_check_first", "risk_notes", "sources", "confidence"],
                "source_ids": source_ids,
                "used_source_ids": source_ids,
                "evidence_card_ids": evidence_card_ids,
                "claim_trace": claim_trace,
                "ranked_steps": ranked_steps,
                "platform_locations": locations,
                "publish_ready": False,
                "used_raw_sources": False,
                "publishing_performed": False,
                "llm_used": False,
                "llm_fallback_used": bool(llm_error),
                "llm_error": llm_error,
            },
            source_ids=source_ids,
        )

    def _run_troubleshooting_writer(
        self,
        request: AgentRunRequest,
        evidence_cards: list[dict],
        ranked_steps: list[dict],
        sources: list[dict],
        llm_error: str | None,
    ) -> AgentRunResponse:
        source_ids = sorted({str(card.get("source_id")) for card in evidence_cards if card.get("source_id")})
        evidence_card_ids = [str(card.get("evidence_card_id")) for card in evidence_cards if card.get("evidence_card_id")]
        claim_trace = [
            {
                "claim": card.get("claim"),
                "source_id": card.get("source_id"),
                "evidence_card_id": card.get("evidence_card_id"),
                "confidence": card.get("confidence"),
            }
            for card in evidence_cards
        ]
        title = f"{request.game_name} {request.topic.title()} Fix"
        lines = [
            f"# {title}",
            "",
            f"If {request.game_name} has {request.topic}, start with reversible fixes. Do not download replacement files or delete saves while you are still narrowing down the cause.",
            "",
            "## Quick Answer",
            "Try the lowest-risk source-backed steps first, then separate platform-specific notes before changing anything deeper.",
            "",
            "## What To Try First",
        ]
        for step in ranked_steps:
            lines.extend(
                [
                    f"{step['rank']}. {step['solution']}",
                    f"Risk: {step.get('risk_level', 'low')}.",
                    f"Sources: {', '.join(step.get('source_ids', []))}",
                ]
            )
        lines.extend(
            [
                "",
                "## Do Not Try First",
                "- Do not download unknown DLL files, recovery tools, or executable replacements.",
                "- Do not delete saves or config folders without a backup.",
                "- Do not apply platform-specific fixes until you confirm they match your setup.",
                "",
                "## Sources",
            ]
        )
        for source in sources:
            lines.append(f"- {source.get('title')} ({source.get('source_type')}): {source.get('url')}")
        lines.extend(
            [
                "",
                "## Confidence",
                "Draft benchmark only. Source trace is present, but this page should remain unpublished until source freshness and platform edge cases are checked.",
            ]
        )
        draft = "\n".join(lines) + "\n"
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "game": request.game_name,
                "player_question": request.topic,
                "draft_format": "markdown",
                "draft_excerpt": draft,
                "markdown": draft,
                "sections": ["quick_answer", "what_to_try_first", "risk_notes", "sources", "confidence"],
                "source_ids": source_ids,
                "used_source_ids": source_ids,
                "evidence_card_ids": evidence_card_ids,
                "claim_trace": claim_trace,
                "ranked_steps": ranked_steps,
                "publish_ready": False,
                "used_raw_sources": False,
                "publishing_performed": False,
                "llm_used": False,
                "llm_fallback_used": bool(llm_error),
                "llm_error": llm_error,
            },
            source_ids=source_ids,
        )

    def _maybe_run_llm_writer(
        self,
        request: AgentRunRequest,
        evidence_cards: list[dict],
        ranked_steps: list[dict],
    ) -> dict[str, object] | None:
        settings = get_settings()
        if not settings.enable_llm_writer:
            return None
        payload = request.payload or {}
        llm_payload = build_llm_writer_payload(
            game=request.game_name,
            player_question=request.topic,
            article_intent=payload.get("article_intent") or f"Help players answer: {request.topic}",
            evidence_cards=evidence_cards,
            ranked_steps=ranked_steps,
            risk_notes=payload.get("risk_notes") or [
                "Back up saves before moving, deleting, editing, or replacing files.",
                "Do not download unknown recovery tools, DLL files, or patches.",
            ],
            uncertainty_notes=payload.get("uncertainty_notes") or [
                "Keep the draft unpublished until verification confirms claim traceability."
            ],
        )
        adapter = self.llm_adapter or OpenAILLMWriterAdapter()
        try:
            return {"ok": True, "output": adapter.generate(llm_payload)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def _response_from_llm_output(
        self,
        request: AgentRunRequest,
        evidence_cards: list[dict],
        ranked_steps: list[dict],
        llm_output: dict,
    ) -> AgentRunResponse:
        source_ids = sorted({str(card.get("source_id")) for card in evidence_cards if card.get("source_id")})
        evidence_card_ids = [str(card.get("evidence_card_id")) for card in evidence_cards if card.get("evidence_card_id")]
        claim_trace = llm_output.get("claim_trace") or [
            {
                "claim": card.get("claim"),
                "source_id": card.get("source_id"),
                "evidence_card_id": card.get("evidence_card_id"),
                "confidence": card.get("confidence"),
            }
            for card in evidence_cards
            if card.get("claim")
        ]
        markdown = str(llm_output.get("markdown") or llm_output.get("draft_excerpt") or "").strip()
        if not markdown:
            raise ValueError("LLM writer returned no markdown.")
        normalized_source_ids = self._normalize_source_ids(llm_output, source_ids)
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "game": request.game_name,
                "player_question": request.topic,
                "draft_format": "markdown",
                "draft_excerpt": markdown,
                "markdown": markdown,
                "sections": ["llm_draft", "risk_notes", "sources"],
                "source_ids": normalized_source_ids,
                "used_source_ids": normalized_source_ids,
                "evidence_card_ids": evidence_card_ids,
                "claim_trace": claim_trace,
                "ranked_steps": ranked_steps,
                "uncertainty_notes": llm_output.get("uncertainty_notes", []),
                "risk_notes": llm_output.get("risk_notes", []),
                "publish_ready": False,
                "used_raw_sources": False,
                "publishing_performed": False,
                "llm_used": True,
                "llm_fallback_used": False,
                "llm_model": llm_output.get("model") or get_settings().llm_model,
            },
            source_ids=normalized_source_ids,
            mock=False,
        )

    @staticmethod
    def _normalize_source_ids(llm_output: dict, fallback_source_ids: list[str]) -> list[str]:
        ids = llm_output.get("used_source_ids")
        if ids is None:
            ids = llm_output.get("source_ids")
        if ids is None:
            ids = fallback_source_ids
        return sorted({str(source_id) for source_id in ids if source_id})
