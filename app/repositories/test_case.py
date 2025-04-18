from typing import List
from bson import ObjectId

from .base import BaseRepository
from database.models.test_case import TestCase


class TestCaseRepository(BaseRepository[TestCase]):
    def __init__(self):
        super().__init__(TestCase)

    @staticmethod
    def find_by_problem(problem_id: str) -> List[TestCase]:
        return TestCase.objects(problem_id=ObjectId(problem_id))

    @staticmethod
    def find_samples_by_problem(problem_id: str) -> List[TestCase]:
        return TestCase.objects(problem_id=ObjectId(problem_id), is_sample=True)

    @staticmethod
    def find_hidden_by_problem(problem_id: str) -> List[TestCase]:
        return TestCase.objects(problem_id=ObjectId(problem_id), is_sample=False)
