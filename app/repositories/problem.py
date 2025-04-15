from typing import List, Optional
from bson import ObjectId
from mongoengine import QuerySet

from .base import BaseRepository
from database.models.problem import Problem
from database.models.test_case import TestCase


class ProblemRepository(BaseRepository[Problem]):
    def __init__(self):
        super().__init__(Problem)

    def find_by_id(self, problem_id: str) -> Optional[Problem]:
        try:
            return Problem.objects.get(id=ObjectId(problem_id))
        except Problem.DoesNotExist:
            return None

    def find_by_title(self, title: str, contest_id: str) -> Optional[Problem]:
        try:
            return Problem.objects.get(title=title, contest_id=ObjectId(contest_id))
        except Problem.DoesNotExist:
            return None

    def find_by_contest(self, contest_id: str) -> List[Problem]:
        return list(Problem.objects(contest_id=ObjectId(contest_id)))

    def find_with_test_cases(self, problem_id: str) -> Optional[Problem]:
        problem = self.find_by_id(problem_id)
        if not problem:
            return None
        problem.test_cases = list(TestCase.objects(problem_id=ObjectId(problem_id)))
        return problem

    def create(self, data: dict) -> Problem:
        problem = Problem(**data)
        problem.save()
        return problem

    def update(self, problem_id: str, data: dict) -> Optional[Problem]:
        problem = self.find_by_id(problem_id)
        if not problem:
            return None
        for key, value in data.items():
            setattr(problem, key, value)
        problem.save()
        return problem

    def delete(self, problem_id: str) -> bool:
        problem = self.find_by_id(problem_id)
        if not problem:
            return False
        problem.delete()
        return True

    def all(self) -> QuerySet:
        return Problem.objects.all()
