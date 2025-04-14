from typing import List, Optional
from bson import ObjectId

from repositories.base import BaseRepository
from database.models.contest import Contest
from database.models.problem import Problem


def find_by_name(name: str) -> Optional[Contest]:
    try:
        return Contest.objects.get(name=name)
    except Contest.DoesNotExist:
        return None


def find_active() -> List[Contest]:
    return Contest.objects.all()


class ContestRepository(BaseRepository[Contest]):
    def __init__(self):
        super().__init__(Contest)

    def find_with_problems(self, contest_id: str) -> Optional[Contest]:
        contest = self.find_by_id(contest_id)
        if not contest:
            return None

        contest.problems = Problem.objects(contest_id=ObjectId(contest_id))
        return contest

