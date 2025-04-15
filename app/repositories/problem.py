from typing import List, Optional
from bson import ObjectId

from .base import BaseRepository
from database.models.problem import Problem
from database.models.test_case import TestCase


def find_by_contest(contest_id: str) -> List[Problem]:
    return Problem.objects(contest_id=ObjectId(contest_id))


def find_by_title(title: str, contest_id: str) -> Optional[Problem]:
    try:
        return Problem.objects.get(title=title, contest_id=ObjectId(contest_id))

    except Problem.DoesNotExist:
        return None


class ProblemRepository(BaseRepository[Problem]):
    def __init__(self):
        super().__init__(Problem)

    def find_with_test_cases(self, problem_id: str) -> Optional[Problem]:
        problem = self.find_by_id(problem_id)

        if not problem:
            return None

        problem.test_cases = TestCase.objects(problem_id=ObjectId(problem_id))

        return problem


def find_by_id(problem_id):
    try:
        return Problem.objects.get(id=ObjectId(problem_id))

    except Problem.DoesNotExist:
        return None
