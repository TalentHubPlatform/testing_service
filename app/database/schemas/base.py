from pydantic import BaseModel
from typing import Any, List, Optional
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Невалидный ObjectId")
        return ObjectId(v)


class MongoBaseModel(BaseModel):
    model_config = {
        "json_encoders": {ObjectId: str},
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }


class GenericResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[Any]
