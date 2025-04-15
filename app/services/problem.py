from typing import Dict, List, Optional, Any
from bson import ObjectId

from repositories import (
    problem_repo,
    contest_repo,
    test_case_repo,
    input_type_repo,
    output_type_repo
)


class ProblemService:
    @staticmethod
    def create_problem(title: str, description: str, contest_id: str,
                       input_type_id: str = None, output_type_id: str = None,
                       time_limit: float = 1.0, memory_limit: int = 256) -> Dict[str, Any]:
        contest = contest_repo.find_by_id(contest_id)
        if not contest:
            return {"success": False, "message": "Contest not found"}

        existing = problem_repo.find_by_title(title, contest_id)

        if existing:
            return {"success": False, "message": "Problem with this title already exists in the contest"}

        if input_type_id and not input_type_repo.find_by_id(input_type_id):
            return {"success": False, "message": "Input type not found"}

        if output_type_id and not output_type_repo.find_by_id(output_type_id):
            return {"success": False, "message": "Output type not found"}

        problem_data = {
            "title": title,
            "description": description,
            "contest_id": ObjectId(contest_id),
            "time_limit": time_limit,
            "memory_limit": memory_limit
        }

        if input_type_id:
            problem_data["input_type_id"] = ObjectId(input_type_id)

        if output_type_id:
            problem_data["output_type_id"] = ObjectId(output_type_id)

        problem = problem_repo.create(problem_data)

        return {
            "success": True,
            "message": "Problem created successfully",
            "problem_id": str(problem.id)
        }

    @staticmethod
    def update_problem(problem_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        problem = problem_repo.find_by_id(problem_id)

        if not problem:
            return {"success": False, "message": "Problem not found"}

        if "title" in data and data["title"] != problem.title:
            existing = problem_repo.find_by_title(data["title"], str(problem.contest_id.id))

            if existing and str(existing.id) != problem_id:
                return {"success": False, "message": "Problem with this title already exists in the contest"}

        if "input_type_id" in data and data["input_type_id"]:
            data["input_type_id"] = ObjectId(data["input_type_id"])

        if "output_type_id" in data and data["output_type_id"]:
            data["output_type_id"] = ObjectId(data["output_type_id"])

        updated_problem = problem_repo.update(problem_id, data)

        if not updated_problem:
            return {"success": False, "message": "Error updating problem"}

        return {
            "success": True,
            "message": "Problem updated successfully",
            "problem_id": problem_id
        }

    @staticmethod
    def delete_problem(problem_id: str) -> Dict[str, Any]:
        problem = problem_repo.find_by_id(problem_id)

        if not problem:
            return {"success": False, "message": "Problem not found"}

        result = problem_repo.delete(problem_id)

        if not result:
            return {"success": False, "message": "Error deleting problem"}

        return {
            "success": True,
            "message": "Problem deleted successfully"
        }

    @staticmethod
    def get_problem(problem_id: str, include_tests: bool = False) -> Optional[Dict[str, Any]]:
        if include_tests:
            problem = problem_repo.find_with_test_cases(problem_id)
        else:
            problem = problem_repo.find_by_id(problem_id)

        if not problem:
            return None

        result = {
            "id": str(problem.id),
            "title": problem.title,
            "description": problem.description,
            "contest_id": str(problem.contest_id.id),
            "time_limit": problem.time_limit,
            "memory_limit": problem.memory_limit
        }

        if hasattr(problem, "input_type_id") and problem.input_type_id:
            result["input_type_id"] = str(problem.input_type_id.id)

        if hasattr(problem, "output_type_id") and problem.output_type_id:
            result["output_type_id"] = str(problem.output_type_id.id)

        if include_tests and hasattr(problem, "test_cases"):
            result["test_cases"] = []

            for test_case in problem.test_cases:
                result["test_cases"].append({
                    "id": str(test_case.id),
                    "input_data": test_case.input_data,
                    "expected_output": test_case.expected_output,
                    "weight": test_case.weight,
                    "is_sample": test_case.is_sample
                })

        return result

    @staticmethod
    def get_problems_by_contest(contest_id: str) -> List[Dict[str, Any]]:
        contest = contest_repo.find_by_id(contest_id)

        if not contest:
            return []

        problems = problem_repo.find_by_contest(contest_id)

        result = []

        for problem in problems:
            result.append({
                "id": str(problem.id),
                "title": problem.title,
                "description": problem.description,
                "time_limit": problem.time_limit,
                "memory_limit": problem.memory_limit
            })

        return result

    @staticmethod
    def add_test_case(problem_id: str, input_data: str, expected_output: str,
                      weight: int = 1, is_sample: bool = False) -> Dict[str, Any]:
        problem = problem_repo.find_by_id(problem_id)

        if not problem:
            return {"success": False, "message": "Problem not found"}

        test_case_data = {
            "problem_id": ObjectId(problem_id),
            "input_data": input_data,
            "expected_output": expected_output,
            "weight": weight,
            "is_sample": is_sample
        }

        test_case = test_case_repo.create(test_case_data)

        return {
            "success": True,
            "message": "Test case added successfully",
            "test_case_id": str(test_case.id)
        }

    @staticmethod
    def update_test_case(test_case_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        test_case = test_case_repo.find_by_id(test_case_id)

        if not test_case:
            return {"success": False, "message": "Test case not found"}

        updated_test_case = test_case_repo.update(test_case_id, data)

        if not updated_test_case:
            return {"success": False, "message": "Error updating test case"}

        return {
            "success": True,
            "message": "Test case updated successfully",
            "test_case_id": test_case_id
        }

    @staticmethod
    def delete_test_case(test_case_id: str) -> Dict[str, Any]:
        test_case = test_case_repo.find_by_id(test_case_id)

        if not test_case:
            return {"success": False, "message": "Test case not found"}

        result = test_case_repo.delete(test_case_id)

        if not result:
            return {"success": False, "message": "Error deleting test case"}

        return {
            "success": True,
            "message": "Test case deleted successfully"
        }

    @staticmethod
    def get_sample_test_cases(problem_id: str) -> List[Dict[str, Any]]:
        problem = problem_repo.find_by_id(problem_id)

        if not problem:
            return []

        test_cases = test_case_repo.find_samples_by_problem(problem_id)

        result = []

        for test_case in test_cases:
            result.append({
                "id": str(test_case.id),
                "input_data": test_case.input_data,
                "expected_output": test_case.expected_output,
                "weight": test_case.weight,
                "is_sample": test_case.is_sample
            })

        return result
