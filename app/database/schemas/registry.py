from .input_type import InputTypeBase, InputTypeCreate, InputTypeUpdate, InputTypeInDB
from .output_type import OutputTypeBase, OutputTypeCreate, OutputTypeUpdate, OutputTypeInDB
from .language import LanguageBase, LanguageCreate, LanguageUpdate, LanguageInDB
from .contest import ContestBase, ContestCreate, ContestUpdate, ContestInDB, ContestWithProblems
from .contest_language import ContestLanguageBase, ContestLanguageCreate, ContestLanguageInDB
from .problem import ProblemBase, ProblemCreate, ProblemUpdate, ProblemInDB, ProblemWithTestCases
from .test_case import TestCaseBase, TestCaseCreate, TestCaseUpdate, TestCaseInDB
from .submission import SubmissionBase, SubmissionCreate, SubmissionUpdate, SubmissionInDB, SubmissionWithResults
from .submission_result import SubmissionResultBase, SubmissionResultCreate, SubmissionResultUpdate, SubmissionResultInDB
from .contest_result import ContestResultBase, ContestResultCreate, ContestResultUpdate, ContestResultInDB

SCHEMA_CLASSES = {
    "input_type": {
        "base": InputTypeBase,
        "create": InputTypeCreate,
        "update": InputTypeUpdate,
        "in_db": InputTypeInDB
    },
    "output_type": {
        "base": OutputTypeBase,
        "create": OutputTypeCreate,
        "update": OutputTypeUpdate,
        "in_db": OutputTypeInDB
    },
    "language": {
        "base": LanguageBase,
        "create": LanguageCreate,
        "update": LanguageUpdate,
        "in_db": LanguageInDB
    },
    "contest": {
        "base": ContestBase,
        "create": ContestCreate,
        "update": ContestUpdate,
        "in_db": ContestInDB,
        "with_problems": ContestWithProblems
    },
    "contest_language": {
        "base": ContestLanguageBase,
        "create": ContestLanguageCreate,
        "in_db": ContestLanguageInDB
    },
    "problem": {
        "base": ProblemBase,
        "create": ProblemCreate,
        "update": ProblemUpdate,
        "in_db": ProblemInDB,
        "with_test_cases": ProblemWithTestCases
    },
    "test_case": {
        "base": TestCaseBase,
        "create": TestCaseCreate,
        "update": TestCaseUpdate,
        "in_db": TestCaseInDB
    },
    "submission": {
        "base": SubmissionBase,
        "create": SubmissionCreate,
        "update": SubmissionUpdate,
        "in_db": SubmissionInDB,
        "with_results": SubmissionWithResults
    },
    "submission_result": {
        "base": SubmissionResultBase,
        "create": SubmissionResultCreate,
        "update": SubmissionResultUpdate,
        "in_db": SubmissionResultInDB
    },
    "contest_result": {
        "base": ContestResultBase,
        "create": ContestResultCreate,
        "update": ContestResultUpdate,
        "in_db": ContestResultInDB
    }
}
