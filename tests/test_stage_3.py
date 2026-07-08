from packages.agents.editor_agent import edit_draft_text
from packages.agents.writer_agent import WriterAgent
from packages.gates.readability_gate import ReadabilityGate
from packages.shared.schemas import AgentRunRequest, ArticleBrief, GateDecision, WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline


def test_article_brief_contains_editorial_structure() -> None:
    result = run_article_pipeline(WorkflowStartRequest(game_name="Example Game", topic="black screen crash on startup"))
    brief = result.article_brief

    assert brief.title
    assert brief.problem_statement
    assert brief.risk_notes
    assert brief.source_summary
    assert all(solution.source_ids or brief.evidence_gaps for solution in brief.ranked_solutions)


def test_article_brief_marks_evidence_gaps_when_evidence_missing() -> None:
    brief = ArticleBrief(source_summary=[], evidence_gaps=["No evidence cards were available for this brief."])

    assert brief.evidence_gaps == ["No evidence cards were available for this brief."]


def test_writer_agent_outputs_template_sections_and_sources() -> None:
    response = WriterAgent().run(AgentRunRequest())
    draft = response.output["draft_excerpt"]

    for section in ["## Short Answer", "## Steps", "## Risk Notes", "## If It Fails", "## Sources"]:
        assert section in draft
    assert "fixture_official_launch_001" in draft
    assert response.output["publishing_performed"] is False


def test_source_backed_crash_pipeline_does_not_use_save_location_template() -> None:
    result = run_article_pipeline(WorkflowStartRequest(game_name="Example Game", topic="crash on startup"))
    draft = result.pipeline_state.draft

    assert draft is not None
    assert "Crash On Startup Fix" in draft.body
    assert "Save File Location" not in draft.body
    assert "Save File Locations" not in draft.body
    assert "Verify game files" in draft.body
    assert result.agent_outputs["writer_agent"]["player_question"] == "crash on startup"
    assert result.agent_outputs["writer_agent"]["publishing_performed"] is False


def test_editor_removes_banned_phrases_and_keeps_risk_notes() -> None:
    before = "This article will explore fixes.\n\n## Risk Notes\nDo not delete saves."
    result = edit_draft_text(before)

    assert "this article will explore" not in str(result["edited_text"]).lower()
    assert result["risk_notes_visible"] is True


def test_readability_gate_fails_banned_filler() -> None:
    brief = ArticleBrief(article_intent="This article will explore startup crashes.")
    result = ReadabilityGate().evaluate(brief)

    assert result.decision == GateDecision.failed
    assert result.blocks_publish is True
