from packages.shared.schemas import RegressionCommand


def default_regression_plan() -> list[RegressionCommand]:
    return [
        RegressionCommand(command="python -m pytest", purpose="Run the full offline regression suite."),
        RegressionCommand(
            command="python -m packages.workflows.article_pipeline",
            purpose="Run the article workflow smoke without live connectors or publishing.",
        ),
    ]

