from typing import List, Optional
from bson import ObjectId

from repositories.base import BaseRepository
from database.models.contest import Contest
from database.models.problem import Problem


class ContestRepository(BaseRepository[Contest]):
    def __init__(self):
        super().__init__(Contest)

    @staticmethod
    def find_by_name(name: str) -> Optional[Contest]:
        try:
            return Contest.objects.get(name=name)
        except Contest.DoesNotExist:
            return None

    @staticmethod
    def find_with_problems(self, contest_id: str) -> Optional[Contest]:
        contest = self.find_by_id(contest_id)
        if not contest:
            return None

        contest.problems = Problem.objects(contest_id=ObjectId(contest_id))

        return contest

    @staticmethod
    def find_active() -> List[Contest]:
        return Contest.objects(is_active=True).all()

    @staticmethod
    def find_by_track(track_id: int, active_only: bool = False) -> List[Contest]:
        query = {'track_id': track_id}

        if active_only:
            query['is_active'] = True

        return Contest.objects(**query).all()
