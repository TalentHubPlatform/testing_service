from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class OutputTypeBase(MongoBaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class OutputTypeCreate(OutputTypeBase):
    pass


class OutputTypeUpdate(MongoBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class OutputTypeInDB(OutputTypeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
