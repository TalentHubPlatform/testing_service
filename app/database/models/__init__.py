from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey

Base = declarative_base()

contest_language_table = Table(
    'contest_language',
    Base.metadata,
    Column('contest_id', Integer, ForeignKey('contest.id'), primary_key=True),
    Column('language_id', Integer, ForeignKey('language.id'), primary_key=True)
)

from .input_type import InputType
from .output_type import OutputType
from .contest import Contest
from .problem import Problem
from .test_case import TestCase
from .language import Language
from .submission import Submission
from .submission_result import SubmissionResult
from .contest_result import ContestResult