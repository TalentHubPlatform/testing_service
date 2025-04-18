from typing import List
from bson import ObjectId

from repositories.base import BaseRepository
from database.models.contest_language import ContestLanguage
from database.models.language import Language


class ContestLanguageRepository(BaseRepository[ContestLanguage]):
    def __init__(self):
        super().__init__(ContestLanguage)

    @staticmethod
    def find_by_contest(contest_id: str) -> List[ContestLanguage]:
        return ContestLanguage.objects(contest_id=ObjectId(contest_id))

    @staticmethod
    def find_languages_for_contest(contest_id: str) -> List[Language]:
        contest_languages = ContestLanguageRepository.find_by_contest(contest_id)
        language_ids = [cl.language_id.id for cl in contest_languages]
        return Language.objects(id__in=language_ids)

    @staticmethod
    def remove_language_from_contest(contest_id: str, language_id: str) -> bool:
        result = ContestLanguage.objects(
            contest_id=ObjectId(contest_id),
            language_id=ObjectId(language_id)
        ).delete()
        return result > 0

    @staticmethod
    def add_language_to_contest(contest_id: str, language_id: str) -> ContestLanguage:
        existing = ContestLanguage.objects(
            contest_id=ObjectId(contest_id),
            language_id=ObjectId(language_id)
        ).first()

        if existing:
            return existing

        contest_language = ContestLanguage(
            contest_id=ObjectId(contest_id),
            language_id=ObjectId(language_id)
        )
        contest_language.save()

        return contest_language
