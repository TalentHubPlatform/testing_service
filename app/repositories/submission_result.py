from typing import List
from bson import ObjectId

from repositories.base import BaseRepository
from database.models.submission_result import SubmissionResult


class SubmissionResultRepository(BaseRepository[SubmissionResult]):
    def __init__(self):
        super().__init__(SubmissionResult)

    @staticmethod
    def clear_for_submission(submission_id: str) -> int:
        results = SubmissionResult.objects(submission_id=ObjectId(submission_id))
        count = results.count()
        results.delete()
        return count

    @staticmethod
    def find_by_submission(submission_id: str) -> List[SubmissionResult]:
        return SubmissionResult.objects(submission_id=ObjectId(submission_id))

    @staticmethod
    def find_accepted_by_submission(submission_id: str) -> List[SubmissionResult]:
        return SubmissionResult.objects(submission_id=ObjectId(submission_id), status="Accepted")
