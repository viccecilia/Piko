import json
import os
import urllib.error
import urllib.request
from typing import Any, Protocol

from packages.shared.config import get_settings


FORBIDDEN_PROMPT_KEYS = {
    "raw_text",
    "credentials",
    "credential",
    "secret",
    "password",
    "api_key",
    "authorization",
    "access_token",
    "refresh_token",
}
MAX_SAFE_STRING = 800


class LLMWriterAdapter(Protocol):
    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return structured writer output or raise a clear error."""


def _safe_string(value: Any, limit: int = MAX_SAFE_STRING) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def _sanitize_for_prompt(value: Any) -> Any:
    if isinstance(value, dict):
        safe: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if any(forbidden in key_text.lower() for forbidden in FORBIDDEN_PROMPT_KEYS):
                continue
            safe[key_text] = _sanitize_for_prompt(item)
        return safe
    if isinstance(value, list):
        return [_sanitize_for_prompt(item) for item in value]
    if isinstance(value, str):
        return _safe_string(value)
    return value


def build_llm_writer_payload(
    *,
    game: str,
    player_question: str,
    article_intent: str,
    evidence_cards: list[dict[str, Any]],
    ranked_steps: list[dict[str, Any]],
    risk_notes: list[str],
    uncertainty_notes: list[str],
) -> dict[str, Any]:
    allowed_cards = [
        {
            "evidence_card_id": card.get("evidence_card_id"),
            "source_id": card.get("source_id"),
            "claim_type": card.get("claim_type"),
            "claim": card.get("claim"),
            "solution": card.get("solution"),
            "platform": card.get("platform"),
            "confidence": card.get("confidence"),
            "risk_note": card.get("risk_note"),
            "snippet": card.get("quote_snippet") or card.get("snippet"),
        }
        for card in evidence_cards
    ]
    allowed_steps = [
        {
            "rank": step.get("rank"),
            "solution": step.get("solution"),
            "confidence": step.get("confidence"),
            "risk_level": step.get("risk_level"),
            "source_ids": step.get("source_ids", []),
            "evidence_card_ids": step.get("evidence_card_ids", []),
        }
        for step in ranked_steps
    ]
    return _sanitize_for_prompt(
        {
            "game": game,
            "player_question": player_question,
            "article_intent": article_intent,
            "evidence_cards": allowed_cards,
            "ranked_steps": allowed_steps,
            "risk_notes": risk_notes,
            "uncertainty_notes": uncertainty_notes,
        }
    )


class OpenAILLMWriterAdapter:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key if api_key is not None else os.getenv("OPENAI_API_KEY")
        self.model = model or settings.llm_model
        self.timeout = settings.llm_timeout_seconds

    def generate(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        request_payload = {
            "model": self.model,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Piko's source-based game guide writer. Use only the provided evidence cards, "
                        "ranked steps, risk notes, uncertainty notes, and source IDs. Do not add claims, sources, "
                        "tests, personal experience, or publishing decisions. Return JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "task": "Write a concise player-facing draft from the bounded evidence payload.",
                            "required_json_fields": [
                                "markdown",
                                "claim_trace",
                                "used_source_ids",
                                "uncertainty_notes",
                                "risk_notes",
                                "publish_ready",
                                "publishing_performed",
                            ],
                            "payload": payload,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(request_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"OpenAI request failed: HTTP {exc.code}") from exc
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        parsed["model"] = self.model
        return parsed
