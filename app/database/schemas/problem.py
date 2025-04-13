from typing import List, Optional
from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class ProblemBase(MongoBaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    contest_id: PyObjectId
    input_type_id: Optional[PyObjectId] = None
    output_type_id: Optional[PyObjectId] = None
    time_limit: float = 1.0
    memory_limit: int = 256


class ProblemCreate(ProblemBase):
    pass


class ProblemUpdate(MongoBaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    input_type_id: Optional[PyObjectId] = None
    output_type_id: Optional[PyObjectId] = None
    time_limit: Optional[float] = None
    memory_limit: Optional[int] = None


class ProblemInDB(ProblemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class TestCaseBase(MongoBaseModel):
    problem_id: PyObjectId
    input_data: Optional[str] = None
    is_sample: bool = False


class TestCaseInDB(TestCaseBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True


class ProblemWithTestCases(ProblemInDB):
    test_cases: List[TestCaseInDB] = []
