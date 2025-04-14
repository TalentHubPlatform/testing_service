from typing import List, Optional
from bson import ObjectId

from repositories.base import BaseRepository
from database.models.contest_result import ContestResult


def find_by_contest(contest_id: str) -> List[ContestResult]:
    return ContestResult.objects(contest_id=ObjectId(contest_id)).order_by('-total_score', 'penalty')


def find_by_user_and_contest(user_id: int, contest_id: str) -> Optional[ContestResult]:
    try:
        return ContestResult.objects.get(user_id=user_id, contest_id=ObjectId(contest_id))

    except ContestResult.DoesNotExist:
        return None


class ContestResultRepository(BaseRepository[ContestResult]):
    def __init__(self):
        super().__init__(ContestResult)

    def update_or_create(self, contest_id: str, user_id: int, data: dict) -> ContestResult:
        try:
            result = ContestResult.objects.get(contest_id=ObjectId(contest_id), user_id=user_id)

            for key, value in data.items():
                setattr(result, key, value)

            result.save()
            return result

        except ContestResult.DoesNotExist:
            data['contest_id'] = ObjectId(contest_id)
            data['user_id'] = user_id
            return self.create(data)
