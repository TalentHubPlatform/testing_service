from typing import List, Optional, Any
from pydantic import Field
from datetime import datetime

from .base import MongoBaseModel, PyObjectId


class SubmissionBase(MongoBaseModel):
    user_id: int
    problem_id: PyObjectId
    contest_id: PyObjectId
    language: str = Field(..., max_length=50)
    code: str


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(MongoBaseModel):
    code: Optional[str] = None
    submission_result_id: Optional[PyObjectId] = None


class SubmissionInDB(SubmissionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    submitted_at: datetime
    submission_result_id: Optional[PyObjectId] = None

    class Config:
        allow_population_by_field_name = True


class SubmissionResultBase(MongoBaseModel):
    submission_id: PyObjectId
    test_case_id: PyObjectId
    status: str


class SubmissionResultInDB(SubmissionResultBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class SubmissionWithResults(SubmissionInDB):
    results: List[SubmissionResultInDB] = []
