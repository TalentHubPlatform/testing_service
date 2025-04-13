from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class InputTypeBase(MongoBaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class InputTypeCreate(InputTypeBase):
    pass


class InputTypeUpdate(MongoBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class InputTypeInDB(InputTypeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
