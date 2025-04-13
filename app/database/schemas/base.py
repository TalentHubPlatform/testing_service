from pydantic import BaseModel
from typing import Any, List, Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")

        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MongoBaseModel(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class GenericResponse(MongoBaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class PaginatedResponse(MongoBaseModel):
    total: int
    page: int
    per_page: int
    items: List[Any]
