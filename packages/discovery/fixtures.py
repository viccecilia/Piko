import json
from pathlib import Path

from packages.shared.schemas import GameHeatSignal, PlayerQuestionSignal


FIXTURE_PATH = Path("fixtures/player_questions/sample_player_questions.json")


def load_discovery_fixtures(path: Path = FIXTURE_PATH) -> tuple[list[GameHeatSignal], list[PlayerQuestionSignal]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    games = [GameHeatSignal(**item) for item in payload.get("games", [])]
    questions = [PlayerQuestionSignal(**item) for item in payload.get("questions", [])]
    return games, questions
