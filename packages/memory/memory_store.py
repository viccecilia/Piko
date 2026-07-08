from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryRecord:
    memory_type: str
    key: str
    value: dict[str, Any]
    game_id: str | None = None
    source_ids: list[str] = field(default_factory=list)
    confidence: int = 0


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str, str | None], MemoryRecord] = {}

    def upsert(self, record: MemoryRecord) -> MemoryRecord:
        self._records[(record.memory_type, record.key, record.game_id)] = record
        return record

    def lookup(self, memory_type: str, key: str, game_id: str | None = None) -> MemoryRecord | None:
        return self._records.get((memory_type, key, game_id))

    def list_by_game(self, game_id: str) -> list[MemoryRecord]:
        return [record for record in self._records.values() if record.game_id == game_id]
