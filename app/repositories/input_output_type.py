from typing import Optional

from repositories.base import BaseRepository
from database.models.input_type import InputType
from database.models.output_type import OutputType


class InputTypeRepository(BaseRepository[InputType]):
    def __init__(self):
        super().__init__(InputType)

    def find_by_name(self, name: str) -> Optional[InputType]:
        try:
            return InputType.objects.get(name=name)

        except InputType.DoesNotExist:
            return None


class OutputTypeRepository(BaseRepository[OutputType]):
    def __init__(self):
        super().__init__(OutputType)

    def find_by_name(self, name: str) -> Optional[OutputType]:
        try:
            return OutputType.objects.get(name=name)

        except OutputType.DoesNotExist:
            return None
