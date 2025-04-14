from typing import List
from .base import BaseRepository
from database.models.contest import Contest


def find_by_event(event_id: int) -> List[Contest]:
    return Contest.objects(event_id=event_id)


def find_by_name(name: str) -> List[Contest]:
    return Contest.objects(name=name)


class ContestRepository(BaseRepository[Contest]):
    def __init__(self):
        super().__init__(Contest)
