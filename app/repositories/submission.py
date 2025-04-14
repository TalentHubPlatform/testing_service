from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from .base import BaseRepository
from database.models.submission import Submission
from database.models.submission_result import SubmissionResult


def find_user_last_submission(user_id: int, problem_id: str) -> Optional[Submission]:
    submissions = Submission.objects(user_id=user_id, problem_id=ObjectId(problem_id)).order_by('-submitted_at')
    return submissions.first() if submissions else None


def find_by_user(user_id: int, skip: int = 0, limit: int = 100) -> List[Submission]:
    return Submission.objects(user_id=user_id).order_by('-submitted_at').skip(skip).limit(limit)


def find_by_problem(problem_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
    return Submission.objects(problem_id=ObjectId(problem_id)).order_by('-submitted_at').skip(skip).limit(limit)


def find_by_contest(contest_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
    return Submission.objects(contest_id=ObjectId(contest_id)).order_by('-submitted_at').skip(skip).limit(limit)


class SubmissionRepository(BaseRepository[Submission]):
    def __init__(self):
        super().__init__(Submission)

    def find_with_results(self, submission_id: str) -> Optional[Submission]:
        submission = self.find_by_id(submission_id)
        if not submission:
            return None

        submission.results = SubmissionResult.objects(submission_id=ObjectId(submission_id))
        return submission

    def create_with_time(self, data: dict) -> Submission:
        if 'submitted_at' not in data:
            data['submitted_at'] = datetime.datetime.now(datetime.UTC)
        return self.create(data)
    