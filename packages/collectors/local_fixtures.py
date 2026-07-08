import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "sources"


class LocalSourceFixture(BaseModel):
    source_id: str
    source_type: str
    url: str
    title: str
    date: str
    game_id: str
    game_name: str
    trust_tier: str
    platform: str
    content: str = Field(max_length=1200)

    def searchable_text(self) -> str:
        return f"{self.game_name} {self.title} {self.platform} {self.content}".lower()


def load_local_source_fixtures(fixture_dir: Path = FIXTURE_DIR) -> list[LocalSourceFixture]:
    fixtures: list[LocalSourceFixture] = []
    for path in sorted(fixture_dir.glob("*.json")):
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        fixtures.append(LocalSourceFixture.model_validate(data))
    return fixtures


def select_local_source_candidates(
    game_name: str,
    player_question: str,
    fixture_dir: Path = FIXTURE_DIR,
) -> list[dict[str, Any]]:
    terms = [term for term in f"{game_name} {player_question}".lower().replace("/", " ").split() if len(term) > 2]
    candidates: list[dict[str, Any]] = []
    for fixture in load_local_source_fixtures(fixture_dir):
        if fixture.game_name.lower() != game_name.lower():
            continue
        haystack = fixture.searchable_text()
        score = sum(1 for term in terms if term in haystack)
        if score <= 0:
            continue
        candidates.append(
            {
                "source_id": fixture.source_id,
                "source_type": fixture.source_type,
                "title": fixture.title,
                "url": fixture.url,
                "trust_tier": fixture.trust_tier,
                "platform": fixture.platform,
                "score": score,
                "reason": f"Matched {score} local fixture terms for '{player_question}'.",
            }
        )
    return sorted(candidates, key=lambda item: (-item["score"], item["source_id"]))


def get_fixtures_by_ids(source_ids: list[str]) -> list[LocalSourceFixture]:
    fixture_map = {fixture.source_id: fixture for fixture in load_local_source_fixtures()}
    return [fixture_map[source_id] for source_id in source_ids if source_id in fixture_map]
