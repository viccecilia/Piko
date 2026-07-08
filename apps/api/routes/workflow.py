from fastapi import APIRouter

from packages.shared.schemas import ArticleWorkflowRequest, WorkflowStartRequest
from packages.workflows.article_pipeline import run_article_pipeline, run_article_workflow
from packages.gates.publishing_eligibility import evaluate_publishing_eligibility
from packages.workflows.verification import verify_workflow_report


router = APIRouter()


@router.post("/article-pipeline/run")
def run_workflow(request: WorkflowStartRequest) -> dict[str, object]:
    return run_article_pipeline(request).model_dump()


@router.post("/article/run")
def run_article(request: ArticleWorkflowRequest) -> dict[str, object]:
    return run_article_workflow(request).model_dump()


@router.post("/article/verify")
def verify_article(report: dict[str, object]) -> dict[str, object]:
    from packages.shared.schemas import WorkflowRunReport

    parsed = WorkflowRunReport.model_validate(report)
    return verify_workflow_report(parsed).model_dump()


@router.post("/article/eligibility")
def publishing_eligibility(report: dict[str, object]) -> dict[str, object]:
    from packages.shared.schemas import WorkflowRunReport

    parsed = WorkflowRunReport.model_validate(report)
    return evaluate_publishing_eligibility(parsed).model_dump()
