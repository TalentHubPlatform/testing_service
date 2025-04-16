from services import contest_service
from fastapi import APIRouter, HTTPException, Path
from starlette import status

incident_router = APIRouter()


@incident_router.post("/track/{track_id}/finish", status_code=status.HTTP_200_OK)
async def finish_track_contests_by_path(
        track_id: int = Path(..., description="ID трека для завершения соревнований"),
):
    result = contest_service.finish_contests_by_track(track_id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {
        "success": True,
        "message": result["message"],
        "finished_count": result["finished_count"]
    }
