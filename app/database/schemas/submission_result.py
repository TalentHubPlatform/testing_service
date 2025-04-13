from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class SubmissionResultBase(MongoBaseModel):
    submission_id: PyObjectId
    test_case_id: PyObjectId
    status: str = Field(..., max_length=50)
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None
    error: Optional[str] = None


class SubmissionResultCreate(SubmissionResultBase):
    pass


class SubmissionResultUpdate(MongoBaseModel):
    status: Optional[str] = Field(None, max_length=50)
    execution_time: Optional[float] = None
    memory_used: Optional[int] = None
    error: Optional[str] = None


class SubmissionResultInDB(SubmissionResultBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
