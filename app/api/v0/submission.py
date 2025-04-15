from typing import List

from core.auth import get_current_user
from services import submission_service
from repositories import submission_repo
from database.schemas.submission import (
    SubmissionCreate,
    SubmissionInDB,
    SubmissionWithResults
)
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from starlette import status

submission_router = APIRouter()


@submission_router.post("/", response_model=SubmissionInDB, status_code=status.HTTP_201_CREATED)
async def create_submission(
        submission: SubmissionCreate,
        background_tasks: BackgroundTasks,
        current_user=Depends(get_current_user)
):
    user_id = current_user["id"]

    result = submission_service.create_submission(
        user_id=user_id,
        problem_id=str(submission.problem_id),
        contest_id=str(submission.contest_id),
        language=submission.language,
        code=submission.code
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    background_tasks.add_task(
        submission_service.judge_submission,
        submission_id=result["submission_id"]
    )

    created_submission = submission_service.get_submission(result["submission_id"])
    if not created_submission:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created submission"
        )

    return {
        "id": created_submission["id"],
        "user_id": created_submission["user_id"],
        "problem_id": created_submission["problem_id"],
        "contest_id": created_submission["contest_id"],
        "language": created_submission["language"],
        "code": created_submission["code"],
        "submitted_at": created_submission["submitted_at"],
        "status": created_submission.get("status", "Pending")
    }


@submission_router.get("/{submission_id}", response_model=SubmissionWithResults)
async def get_submission(
        submission_id: str,
        current_user=Depends(get_current_user)
):
    submission = submission_service.get_submission(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )

    if submission["user_id"] != current_user["id"] and not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this submission"
        )

    return {
        "id": submission["id"],
        "user_id": submission["user_id"],
        "problem_id": submission["problem_id"],
        "contest_id": submission["contest_id"],
        "language": submission["language"],
        "code": submission["code"],
        "submitted_at": submission["submitted_at"],
        "status": submission.get("status", "Unknown"),
        "results": submission.get("results", [])
    }


@submission_router.get("/", response_model=List[SubmissionInDB])
async def get_user_submissions(
        skip: int = Query(0, description="Skip items"),
        limit: int = Query(20, description="Limit items"),
        current_user=Depends(get_current_user)
):
    user_id = current_user["id"]

    submissions = submission_service.get_user_submissions(user_id, skip, limit)
    return submissions


@submission_router.get("/contest/{contest_id}", response_model=List[SubmissionInDB])
async def get_contest_submissions(
        contest_id: str,
        skip: int = Query(0, description="Skip items"),
        limit: int = Query(20, description="Limit items")
):
    submissions_list = submission_repo.find_by_contest(contest_id, skip, limit)

    result = []
    for sub in submissions_list:
        result.append({
            "id": str(sub.id),
            "user_id": sub.user_id,
            "problem_id": str(sub.problem_id.id),
            "contest_id": str(sub.contest_id.id),
            "language": sub.language,
            "code": sub.code,
            "submitted_at": sub.submitted_at,
            "status": getattr(sub, "status", "Unknown")
        })

    return result


@submission_router.get("/problem/{problem_id}", response_model=List[SubmissionInDB])
async def get_problem_submissions(
        problem_id: str,
        skip: int = Query(0, description="Skip items"),
        limit: int = Query(20, description="Limit items")
):
    submissions_list = submission_repo.find_by_problem(problem_id, skip, limit)

    result = []
    for sub in submissions_list:
        result.append({
            "id": str(sub.id),
            "user_id": sub.user_id,
            "problem_id": str(sub.problem_id.id),
            "contest_id": str(sub.contest_id.id),
            "language": sub.language,
            "code": sub.code,
            "submitted_at": sub.submitted_at,
            "status": getattr(sub, "status", "Unknown")
        })

    return result


@submission_router.post("/{submission_id}/rejudge", response_model=SubmissionInDB)
async def rejudge_submission(
        submission_id: str,
        background_tasks: BackgroundTasks
):
    sub = submission_service.get_submission(submission_id)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found"
        )

    background_tasks.add_task(
        submission_service.judge_submission,
        submission_id=submission_id
    )

    submission_repo.update(submission_id, {"status": "Rejudging"})

    updated_sub = submission_service.get_submission(submission_id)

    return {
        "id": updated_sub["id"],
        "user_id": updated_sub["user_id"],
        "problem_id": updated_sub["problem_id"],
        "contest_id": updated_sub["contest_id"],
        "language": updated_sub["language"],
        "code": updated_sub["code"],
        "submitted_at": updated_sub["submitted_at"],
        "status": "Rejudging"
    }
