from mongoengine import connect
import os

from .input_type import InputType
from .output_type import OutputType
from .language import Language
from .contest import Contest
from .contest_language import ContestLanguage
from .problem import Problem
from .test_case import TestCase
from .submission import Submission
from .submission_result import SubmissionResult
from .contest_result import ContestResult

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/contest_db')


def init_db():
    connect(host=MONGO_URI)
