from pydantic import Field

from .base import MongoBaseModel, PyObjectId


class ContestLanguageBase(MongoBaseModel):
    contest_id: PyObjectId
    language_id: PyObjectId


class ContestLanguageCreate(ContestLanguageBase):
    pass


class ContestLanguageInDB(ContestLanguageBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
