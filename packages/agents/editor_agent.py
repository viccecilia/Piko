import re

from packages.agents.base import BaseAgent
from packages.shared.schemas import AgentDefinition, AgentRunRequest, AgentRunResponse


BANNED_FILLER = [
    "in today's gaming landscape",
    "this article will explore",
    "delve into",
    "as an ai",
    "i tested",
]


def edit_draft_text(text: str) -> dict[str, object]:
    edited = text
    removed: list[str] = []
    for phrase in BANNED_FILLER:
        if phrase in edited.lower():
            removed.append(phrase)
            edited = re.sub(re.escape(phrase), "", edited, flags=re.IGNORECASE)
    if "Risk:" not in edited and "Risk Notes" not in edited:
        edited += "\n\n## Risk Notes\nKeep risky changes out of the first steps."
    return {"edited_text": edited.strip(), "removed_patterns": removed, "risk_notes_visible": "Risk" in edited}


class EditorAgent(BaseAgent):
    definition = AgentDefinition(
        name="editor_agent",
        label="Editor Agent",
        purpose="Remove filler, strengthen judgment, and keep the page player-first.",
    )

    def run(self, request: AgentRunRequest) -> AgentRunResponse:
        draft = request.payload.get("draft", "") if request.payload else ""
        edit_result = edit_draft_text(draft) if draft else {
            "edited_text": "",
            "removed_patterns": ["generic_intro", "unsupported_claims"],
            "risk_notes_visible": True,
        }
        return AgentRunResponse(
            agent=self.definition.name,
            output={
                "style_pass": True,
                **edit_result,
                "editor_note": "Mock draft starts with the answer and preserves risk warnings.",
            },
        )
