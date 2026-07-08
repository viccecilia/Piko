import pytest

from packages.shared.schemas import MultiGameJob, WorkflowStartRequest
from packages.shared.token_monitor import TokenMonitor, TokenUsage
from packages.workflows.article_pipeline import run_article_pipeline


def test_multi_game_workflow_sources_stay_separated() -> None:
    example = run_article_pipeline(WorkflowStartRequest(game_id="game_mock_001", game_name="Example Game", topic="crash on startup"))
    other = run_article_pipeline(WorkflowStartRequest(game_id="game_mock_002", game_name="Other Game", topic="crash on startup"))

    example_sources = {source.source_id for source in example.pipeline_state.sources}
    other_sources = {source.source_id for source in other.pipeline_state.sources}
    assert example.pipeline_state.game.game_id == "game_mock_001"
    assert other.pipeline_state.game.game_id == "game_mock_002"
    assert example_sources != other_sources


def test_multi_game_job_rejects_missing_game_id() -> None:
    with pytest.raises(Exception):
        MultiGameJob(job_id="job_1", game_id="", game_name="Example Game", question_cluster="launch issues")


def test_token_monitor_aggregates_by_component() -> None:
    monitor = TokenMonitor()
    monitor.record(TokenUsage(component="writer", prompt_tokens=10, completion_tokens=5))
    monitor.record(TokenUsage(component="writer", prompt_tokens=3, completion_tokens=2))
    monitor.record(TokenUsage(component="editor", prompt_tokens=4, completion_tokens=1))

    assert monitor.summary()["total_tokens"] == 25
    assert monitor.by_component() == {"writer": 20, "editor": 5}


def test_workflow_includes_monitoring_summary_without_secrets() -> None:
    report = run_article_pipeline(WorkflowStartRequest())

    assert report.pipeline_state.monitoring_summary is not None
    assert report.pipeline_state.monitoring_summary.estimated_tokens >= 0
    assert "secret" not in report.pipeline_state.monitoring_summary.model_dump_json().lower()


def test_operations_notes_exist_without_auto_deploy() -> None:
    text = open("docs/operations.md", encoding="utf-8").read().lower()

    assert "backup" in text
    assert "rollback" in text
    assert "no deployment is performed" in text
    assert "automatically" in text
