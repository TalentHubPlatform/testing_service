from typing import List

from services import contest_service
from database.schemas.contest import (
    ContestCreate,
    ContestUpdate,
    ContestInDB,
    ContestWithProblems
)
from database.schemas.contest_result import ContestResultInDB
from fastapi import APIRouter, HTTPException, Query
from starlette import status

contest_router = APIRouter()


@contest_router.get("/", response_model=List[ContestInDB])
async def get_contests(
        skip: int = Query(0, description="Skip items"),
        limit: int = Query(20, description="Limit items")
):
    return contest_service.get_contests(skip, limit)


@contest_router.get("/{contest_id}", response_model=ContestWithProblems)
async def get_contest_by_id(contest_id: str):
    contest = contest_service.get_contest(contest_id)

    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found"
        )

    return contest


@contest_router.post("/", response_model=ContestInDB, status_code=status.HTTP_201_CREATED)
async def create_contest(
        contest: ContestCreate
):
    result = contest_service.create_contest(
        name=contest.name,
        description=contest.description,
        event_id=contest.event_id,
        date_id=contest.date_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    created_contest = contest_service.get_contest(result["contest_id"])

    if not created_contest:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve created contest"
        )

    return created_contest


@contest_router.put("/{contest_id}", response_model=ContestInDB)
async def update_contest(
        contest_id: str,
        contest: ContestUpdate
):
    data = contest.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    result = contest_service.update_contest(contest_id, data)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    updated_contest = contest_service.get_contest(contest_id)

    if not updated_contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found after update"
        )

    return updated_contest


@contest_router.delete("/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contest(
        contest_id: str
):
    result = contest_service.delete_contest(contest_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return None


@contest_router.get("/{contest_id}/results", response_model=List[ContestResultInDB])
async def get_contest_results(contest_id: str):
    contest = contest_service.get_contest(contest_id)

    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found"
        )

    results = contest_service.get_contest_results(contest_id)

    return results


@contest_router.post("/{contest_id}/languages/{language_id}", status_code=status.HTTP_200_OK)
async def add_language_to_contest(
        contest_id: str,
        language_id: str
):
    result = contest_service.add_language_to_contest(contest_id, language_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {"message": result["message"]}


@contest_router.delete("/{contest_id}/languages/{language_id}", status_code=status.HTTP_200_OK)
async def remove_language_from_contest(
        contest_id: str,
        language_id: str
):
    result = contest_service.remove_language_from_contest(contest_id, language_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {"message": result["message"]}
