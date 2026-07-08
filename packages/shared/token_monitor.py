from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    component: str
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class TokenMonitor:
    def __init__(self) -> None:
        self._events: list[TokenUsage] = []

    def record(self, usage: TokenUsage) -> None:
        self._events.append(usage)

    def summary(self) -> dict[str, int]:
        return {
            "events": len(self._events),
            "total_tokens": sum(event.total_tokens for event in self._events),
        }

    def by_component(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for event in self._events:
            totals[event.component] = totals.get(event.component, 0) + event.total_tokens
        return totals
