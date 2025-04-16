from fastapi import APIRouter

from .contest import contest_router
from .problem import problem_router
from .submission import submission_router
from .incident import incident_router

main_v0_router = APIRouter(prefix="/api/v0")
main_v0_router.include_router(contest_router, prefix="/contest", tags=["contest"])
main_v0_router.include_router(problem_router, prefix="/problem", tags=["problem"])
main_v0_router.include_router(submission_router, prefix="/submission", tags=["submission"])
main_v0_router.include_router(incident_router, prefix="/incident", tags=["incident"])
