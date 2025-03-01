from contextlib import asynccontextmanager
from typing import Callable, Dict, Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from src.core.settings import settings
from src.core.models import Base
from src.core.config.db_config import DBConfigurer


class AppConfigurer:

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # async with DBConfigurer.engine.begin() as conn:               ### NO NEED AFTER ALEMBIC ADDED
        #     await conn.run_sync(Base.metadata.create_all)
        yield


    @staticmethod
    def create_app(docs_url, redoc_url) -> FastAPI:
        app = FastAPI(
            lifespan=AppConfigurer.lifespan,
            docs_url=docs_url,
            redoc_url=redoc_url,
        )
        return app

    @staticmethod
    def get_custom_openapi(subject: FastAPI) -> Callable[[], Dict[str, Any]]:
        def custom_openapi() -> Dict[str, Any]:
            if subject.openapi_schema:
                return subject.openapi_schema
            openapi_schema = get_openapi(
                title=settings.app.APP_TITLE,
                version=settings.app.APP_VERSION,
                description=settings.app.APP_DESCRIPTION,
                routes=subject.routes,
            )
            subject.openapi_schema = openapi_schema
            return subject.openapi_schema

        return custom_openapi

    @staticmethod
    def config_validation_exception_handler(app: FastAPI):
        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc: RequestValidationError):
            return JSONResponse(
                status_code=settings.app.APP_422_CODE_STATUS,
                content={"detail": exc.errors(), "body": exc.body},
            )
