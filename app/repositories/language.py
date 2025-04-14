from typing import List, Optional

from repositories.base import BaseRepository
from database.models.language import Language


def find_by_name(name: str) -> Optional[Language]:
    try:
        return Language.objects.get(name=name)
    except Language.DoesNotExist:
        return None


def find_by_name_and_version(name: str, version: str) -> Optional[Language]:
    try:
        return Language.objects.get(name=name, version=version)
    except Language.DoesNotExist:
        return None


def find_active() -> List[Language]:
    return Language.objects.all()


class LanguageRepository(BaseRepository[Language]):
    def __init__(self):
        super().__init__(Language)
    