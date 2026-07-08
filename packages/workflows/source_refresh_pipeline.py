from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SourceFreshness:
    source_id: str
    last_seen: date
    current_seen: date


@dataclass(frozen=True)
class RefreshSignal:
    source_id: str
    needs_refresh: bool
    reason: str


def evaluate_refresh_signals(sources: list[SourceFreshness]) -> list[RefreshSignal]:
    signals: list[RefreshSignal] = []
    for source in sources:
        changed = source.current_seen > source.last_seen
        signals.append(
            RefreshSignal(
                source_id=source.source_id,
                needs_refresh=changed,
                reason="Source changed after article check." if changed else "Source unchanged.",
            )
        )
    return signals
