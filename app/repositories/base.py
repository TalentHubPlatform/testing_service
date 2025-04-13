from typing import List, Optional, Type, TypeVar, Dict, Any, Generic
from bson import ObjectId
from mongoengine import Document, QuerySet

ModelType = TypeVar("ModelType", bound=Document)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType]):
        self.model_class = model_class

    def find_by_id(self, id: str) -> Optional[ModelType]:
        try:
            return self.model_class.objects.get(id=ObjectId(id))

        except (self.model_class.DoesNotExist, ValueError):
            return None

    def find_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.model_class.objects.skip(skip).limit(limit)

    def count(self, **kwargs) -> int:
        return self.model_class.objects(**kwargs).count()

    def create(self, data: Dict[str, Any]) -> ModelType:
        document = self.model_class(**data)
        document.save()

        return document

    def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        document = self.find_by_id(id)

        if document:
            for key, value in data.items():
                setattr(document, key, value)

            document.save()
            return document

        return None

    def delete(self, id: str) -> bool:
        document = self.find_by_id(id)

        if document:
            document.delete()
            return True

        return False

    def find(self, **kwargs) -> QuerySet:
        return self.model_class.objects(**kwargs)
