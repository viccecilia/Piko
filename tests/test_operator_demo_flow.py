import json
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from packages.shared.config import get_settings
from packages.workflows.demo_run import run_operator_demo


client = TestClient(app)


def test_fixture_demo_helper_writes_required_artifacts_without_network_or_llm(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "false")
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "false")
    get_settings.cache_clear()

    def fail_connector(*args, **kwargs):
        raise AssertionError("fixture demo must not call real source connector")

    def fail_llm(*args, **kwargs):
        raise AssertionError("fixture demo must not call LLM writer")

    monkeypatch.setattr("packages.collectors.pcgamingwiki.PCGamingWikiConnector.search", fail_connector)
    monkeypatch.setattr("packages.agents.adapters.llm_writer_adapter.OpenAILLMWriterAdapter.generate", fail_llm)

    artifact = run_operator_demo(
        game_name="Example Game",
        player_question="crash on startup",
        mode="fixture",
        use_llm_writer=False,
        output_dir=str(tmp_path),
    )

    assert artifact["game_name"] == "Example Game"
    assert artifact["player_question"] == "crash on startup"
    assert artifact["mode"] == "fixture"
    assert artifact["draft"]
    assert artifact["sources"]
    assert artifact["evidence_cards"]
    assert artifact["ranked_steps"]
    assert artifact["agent_trace"]
    assert artifact["verification_report"]["status"] == "pass"
    assert artifact["publish_ready"] is False
    assert artifact["publishing_performed"] is False
    assert artifact["real_collection_performed"] is False
    assert artifact["llm_used"] is False
    assert Path(artifact["artifact_paths"]["json"]).exists()
    assert Path(artifact["artifact_paths"]["markdown"]).exists()

    saved = json.loads(Path(artifact["artifact_paths"]["json"]).read_text(encoding="utf-8"))
    assert saved["publish_ready"] is False
    assert saved["publishing_performed"] is False


def test_demo_api_returns_artifact_path(monkeypatch) -> None:
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "false")
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "false")
    get_settings.cache_clear()

    response = client.post(
        "/demo/run",
        json={
            "game_name": "Example Game",
            "player_question": "crash on startup",
            "mode": "fixture",
            "use_llm_writer": False,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["artifact_paths"]["json"].endswith(".json")
    assert payload["artifact_paths"]["markdown"].endswith(".md")
    assert Path(payload["artifact_paths"]["json"]).exists()
    assert payload["publish_ready"] is False
    assert payload["publishing_performed"] is False
    assert payload["llm_used"] is False


def test_demo_real_source_requires_explicit_connector_enable(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PIKO_ENABLE_REAL_CONNECTORS", "false")
    get_settings.cache_clear()

    try:
        run_operator_demo(
            game_name="Hades",
            player_question="Where is the save file location?",
            mode="real-source",
            use_llm_writer=False,
            output_dir=str(tmp_path),
        )
    except ValueError as exc:
        assert "PIKO_ENABLE_REAL_CONNECTORS=true" in str(exc)
    else:
        raise AssertionError("real-source demo should require explicit connector opt-in")

    response = client.post(
        "/demo/run",
        json={
            "game_name": "Hades",
            "player_question": "Where is the save file location?",
            "mode": "real-source",
            "use_llm_writer": False,
        },
    )
    assert response.status_code == 400
    assert "PIKO_ENABLE_REAL_CONNECTORS=true" in response.json()["detail"]


def test_demo_llm_request_falls_back_when_llm_not_enabled(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("PIKO_ENABLE_LLM_WRITER", "false")
    get_settings.cache_clear()

    def fail_llm(*args, **kwargs):
        raise AssertionError("LLM writer should not be called when config is disabled")

    monkeypatch.setattr("packages.agents.adapters.llm_writer_adapter.OpenAILLMWriterAdapter.generate", fail_llm)

    artifact = run_operator_demo(
        game_name="Example Game",
        player_question="crash on startup",
        mode="fixture",
        use_llm_writer=True,
        output_dir=str(tmp_path),
    )

    assert artifact["llm_used"] is False
    assert artifact["publish_ready"] is False
    assert artifact["publishing_performed"] is False
