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


def find_by_id(contest_id=None) -> Optional[Contest]:
    try:
        return Contest.objects.get(id=ObjectId(contest_id))
    except Contest.DoesNotExist:
        return None


class ContestRepository(BaseRepository[Contest]):
    def __init__(self):
        super().__init__(Contest)

    def find_with_problems(self, contest_id: str) -> Optional[Contest]:
        contest = self.find_by_id(contest_id)
        if not contest:
            return None

        contest.problems = Problem.objects(contest_id=ObjectId(contest_id))
        return contest


def create(contest_data):
    contest = Contest(**contest_data)
    contest.save()

    return contest


def update(contest_id, data):
    contest = find_by_id(contest_id)
    if not contest:
        return None

    for key, value in data.items():
        setattr(contest, key, value)

    contest.save()

    return contest


def delete(contest_id):
    contest = find_by_id(contest_id)

    if not contest:
        return False

    contest.delete()

    return True


def find_with_problems(contest_id):
    contest = find_by_id(contest_id)

    if not contest:
        return None

    contest.problems = Problem.objects(contest_id=ObjectId(contest_id))

    return contest


def find_all(skip, limit):
    contests = Contest.objects.skip(skip).limit(limit)
    return contests
