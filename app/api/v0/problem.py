from typing import List

from services import problem_service
from database.schemas.problem import (
    ProblemCreate,
    ProblemUpdate,
    ProblemInDB,
    ProblemWithTestCases,
    TestCaseBase,
    TestCaseInDB
)
from fastapi import APIRouter, HTTPException, Query, Path
from starlette import status

problem_router = APIRouter()


@problem_router.get("/contest/{contest_id}", response_model=List[ProblemInDB])
async def get_problems_by_contest(
        contest_id: str = Path(..., description="ID соревнования")
):
    problems = problem_service.get_problems_by_contest(contest_id)
    return problems


@problem_router.get("/{problem_id}", response_model=ProblemWithTestCases)
async def get_problem(
        problem_id: str,
        include_tests: bool = Query(False, description="Включать ли тестовые случаи в ответ")
):
    problem = problem_service.get_problem(problem_id, include_tests)

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found"
        )

    return problem


@problem_router.post("/", response_model=ProblemInDB, status_code=status.HTTP_201_CREATED)
async def create_problem(
        problem: ProblemCreate
):
    result = problem_service.create_problem(
        title=problem.title,
        description=problem.description,
        contest_id=str(problem.contest_id),
        input_type_id=str(problem.input_type_id) if problem.input_type_id else None,
        output_type_id=str(problem.output_type_id) if problem.output_type_id else None,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    created_problem = problem_service.get_problem(result["problem_id"])
    if not created_problem:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created problem"
        )

    return created_problem


@problem_router.put("/{problem_id}", response_model=ProblemInDB)
async def update_problem(
        problem_id: str,
        problem: ProblemUpdate
):
    data = problem.model_dump(exclude_unset=True, exclude_none=True)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    if 'input_type_id' in data and data['input_type_id']:
        data['input_type_id'] = str(data['input_type_id'])

    if 'output_type_id' in data and data['output_type_id']:
        data['output_type_id'] = str(data['output_type_id'])

    result = problem_service.update_problem(problem_id, data)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    updated_problem = problem_service.get_problem(problem_id)
    if not updated_problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found after update"
        )

    return updated_problem


@problem_router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_problem(
        problem_id: str
):
    result = problem_service.delete_problem(problem_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return None


@problem_router.post("/{problem_id}/test-cases", response_model=TestCaseInDB, status_code=status.HTTP_201_CREATED)
async def add_test_case(
        problem_id: str,
        test_case: TestCaseBase
):
    test_case_data = test_case.model_dump()
    test_case_data["problem_id"] = problem_id

    if not isinstance(test_case, TestCaseBase):
        raise TypeError("test_case must be an instance of TestCaseBase")

    result = problem_service.add_test_case(
        problem_id=problem_id,
        input_data=test_case.input_data or "",
        expected_output=getattr(test_case, "expected_output", ""),
        weight=getattr(test_case, "weight", 1),
        is_sample=test_case.is_sample
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {
        "id": result["test_case_id"],
        "problem_id": problem_id,
        "input_data": test_case.input_data,
        "is_sample": test_case.is_sample
    }


@problem_router.put("/test-cases/{test_case_id}", response_model=TestCaseInDB)
async def update_test_case(
        test_case_id: str,
        test_case: TestCaseBase
):
    data = {k: v for k, v in test_case.model_dump().items() if k != "problem_id" and v is not None}

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    result = problem_service.update_test_case(test_case_id, data)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {
        "id": test_case_id,
        "problem_id": test_case.problem_id,
        "input_data": test_case.input_data,
        "is_sample": test_case.is_sample
    }


@problem_router.delete("/test-cases/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case(
        test_case_id: str
):
    result = problem_service.delete_test_case(test_case_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return None


@problem_router.get("/{problem_id}/sample-test-cases", response_model=List[TestCaseInDB])
async def get_sample_test_cases(
        problem_id: str
):
    samples = problem_service.get_sample_test_cases(problem_id)
    return samples
