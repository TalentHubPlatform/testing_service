from contextlib import asynccontextmanager

from api.v0.main import main_v0_router
from core.config import settings
from database.session import sessionmanager
from fastapi import FastAPI


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(
            str(settings.db.url),
            settings.db.db_name
        )

        @asynccontextmanager
        async def lifespan(app):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    server = FastAPI(
        title="FastAPI server",
        docs_url="/api/docs",
        openapi_url="/api",
        lifespan=lifespan,
    )
    server.include_router(main_v0_router)

    return server
