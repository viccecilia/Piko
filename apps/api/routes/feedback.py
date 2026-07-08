from fastapi import APIRouter

from apps.api.services.feedback import feedback_repository
from packages.shared.schemas import FeedbackRequest


router = APIRouter()


@router.post("")
def submit_feedback(request: FeedbackRequest) -> dict[str, object]:
    return feedback_repository.save(request).model_dump()

