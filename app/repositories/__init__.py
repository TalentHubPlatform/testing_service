from .base import BaseRepository
from .contest import ContestRepository
from .contest_language import ContestLanguageRepository
from .contest_result import ContestResultRepository
from .input_output_type import InputTypeRepository, OutputTypeRepository
from .language import LanguageRepository
from .problem import ProblemRepository
from .test_case import TestCaseRepository
from .submission import SubmissionRepository
from .submission_result import SubmissionResultRepository

contest_repo = ContestRepository()
contest_language_repo = ContestLanguageRepository()
contest_result_repo = ContestResultRepository()
input_type_repo = InputTypeRepository()
output_type_repo = OutputTypeRepository()
language_repo = LanguageRepository()
problem_repo = ProblemRepository()
test_case_repo = TestCaseRepository()
submission_repo = SubmissionRepository()
submission_result_repo = SubmissionResultRepository()
