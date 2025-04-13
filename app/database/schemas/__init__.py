from .base import MongoBaseModel, PyObjectId, GenericResponse, PaginatedResponse

from .input_type import InputTypeBase, InputTypeCreate, InputTypeUpdate, InputTypeInDB
from .output_type import OutputTypeBase, OutputTypeCreate, OutputTypeUpdate, OutputTypeInDB
from .language import LanguageBase, LanguageCreate, LanguageUpdate, LanguageInDB
from .contest import ContestBase, ContestCreate, ContestUpdate, ContestInDB
from .contest_language import ContestLanguageBase, ContestLanguageCreate, ContestLanguageInDB
from .problem import ProblemBase, ProblemCreate, ProblemUpdate, ProblemInDB
from .test_case import TestCaseBase, TestCaseCreate, TestCaseUpdate, TestCaseInDB
from .submission import SubmissionBase, SubmissionCreate, SubmissionUpdate, SubmissionInDB
from .submission_result import SubmissionResultBase, SubmissionResultCreate, SubmissionResultUpdate, SubmissionResultInDB
from .contest_result import ContestResultBase, ContestResultCreate, ContestResultUpdate, ContestResultInDB

from .contest import ContestWithProblems
from .problem import ProblemWithTestCases
from .submission import SubmissionWithResults

from .registry import SCHEMA_CLASSES
