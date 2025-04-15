from typing import Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class TestCaseBase(MongoBaseModel):
    problem_id: PyObjectId
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    weight: Optional[int] = 1
    is_sample: bool = False


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(MongoBaseModel):
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    weight: Optional[int] = None
    is_sample: Optional[bool] = None


class TestCaseInDB(TestCaseBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
