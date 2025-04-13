from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class ContestResultBase(MongoBaseModel):
    contest_id: PyObjectId
    user_id: int
    total_score: int = 0
    solved_score: int = 0
    penalty: int = 0


class ContestResultCreate(ContestResultBase):
    pass


class ContestResultUpdate(MongoBaseModel):
    total_score: Optional[int] = None
    solved_score: Optional[int] = None
    penalty: Optional[int] = None


class ContestResultInDB(ContestResultBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
