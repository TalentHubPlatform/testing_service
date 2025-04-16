from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from .base import BaseRepository
from database.models.submission import Submission
from database.models.submission_result import SubmissionResult


class SubmissionRepository(BaseRepository[Submission]):
    def __init__(self):
        super().__init__(Submission)

    @staticmethod
    def find_user_last_submission(user_id: int, problem_id: str) -> Optional[Submission]:
        submissions = Submission.objects(user_id=user_id, problem_id=ObjectId(problem_id)).order_by('-submitted_at')
        return submissions.first() if submissions else None

    @staticmethod
    def find_by_user(user_id: int, skip: int = 0, limit: int = 100) -> List[Submission]:
        return Submission.objects(user_id=user_id).order_by('-submitted_at').skip(skip).limit(limit)

    @staticmethod
    def find_by_problem(problem_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
        return Submission.objects(problem_id=ObjectId(problem_id)).order_by('-submitted_at').skip(skip).limit(limit)

    @staticmethod
    def find_by_contest(contest_id: str, skip: int = 0, limit: int = 100) -> List[Submission]:
        return Submission.objects(contest_id=ObjectId(contest_id)).order_by('-submitted_at').skip(skip).limit(limit)

    @staticmethod
    def create(submission_data: dict) -> Submission:
        submission = Submission(**submission_data)
        submission.save()
        return submission

    @staticmethod
    def find(user_id: int, problem_id: str, contest_id: str) -> Optional[Submission]:
        try:
            return Submission.objects.get(
                user_id=user_id,
                problem_id=ObjectId(problem_id),
                contest_id=ObjectId(contest_id)
            )
        except Submission.DoesNotExist:
            return None

    @staticmethod
    def find_by_id(submission_id: str) -> Optional[Submission]:
        try:
            return Submission.objects.get(id=ObjectId(submission_id))
        except Submission.DoesNotExist:
            return None

    @staticmethod
    def update(submission_id: str, param: dict) -> Optional[Submission]:
        try:
            submission = Submission.objects.get(id=ObjectId(submission_id))
        except Submission.DoesNotExist:
            return None

        for key, value in param.items():
            setattr(submission, key, value)

        submission.save()
        return submission

    @staticmethod
    def find_with_results(submission_id: str) -> Optional[Submission]:
        try:
            submission = Submission.objects.get(id=ObjectId(submission_id))
        except Submission.DoesNotExist:
            return None

        submission.results = SubmissionResult.objects(submission_id=ObjectId(submission_id))
        return submission

    @staticmethod
    def create_with_time(data: dict) -> Submission:
        if 'submitted_at' not in data:
            data['submitted_at'] = datetime.now(datetime.UTC)
        return SubmissionRepository.create(data)
