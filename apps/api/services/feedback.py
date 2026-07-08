from packages.shared.schemas import FeedbackRecord, FeedbackRequest


class InMemoryFeedbackRepository:
    def __init__(self) -> None:
        self._records: list[FeedbackRecord] = []

    def save(self, request: FeedbackRequest) -> FeedbackRecord:
        record = FeedbackRecord(
            **request.model_dump(),
            feedback_id=f"feedback_{len(self._records) + 1:04d}",
            stored_as_signal_only=True,
        )
        self._records.append(record)
        return record

    def list(self) -> list[FeedbackRecord]:
        return list(self._records)


feedback_repository = InMemoryFeedbackRepository()

