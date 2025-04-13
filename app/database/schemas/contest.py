from typing import List, Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class ContestBase(MongoBaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    event_id: Optional[int] = None
    date_id: Optional[int] = None


class ContestCreate(ContestBase):
    pass


class ContestUpdate(MongoBaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    event_id: Optional[int] = None
    date_id: Optional[int] = None


class ContestInDB(ContestBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class ProblemBase(MongoBaseModel):
    title: str
    description: Optional[str] = None
    contest_id: PyObjectId


class ProblemInDB(ProblemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class LanguageBase(MongoBaseModel):
    name: str
    version: Optional[str] = None


class LanguageInDB(LanguageBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class ContestWithProblems(ContestInDB):
    problems: List[ProblemInDB] = []
    languages: List[LanguageInDB] = []
