from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class LanguageBase(MongoBaseModel):
    name: str = Field(..., max_length=100)
    version: Optional[str] = Field(None, max_length=50)


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(MongoBaseModel):
    name: Optional[str] = Field(None, max_length=100)
    version: Optional[str] = Field(None, max_length=50)


class LanguageInDB(LanguageBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
