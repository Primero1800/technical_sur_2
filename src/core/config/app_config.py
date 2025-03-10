import logging
from contextlib import asynccontextmanager
from typing import Callable, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import JSONResponse

from src import errors
from src.core.settings import settings


class AppConfigurer:

    logging.basicConfig(
        level=logging.INFO,
        format=settings.logging.LOGGING_FORMAT
    )

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
            error_message = exc.errors()
            logging.log(level=logging.INFO, msg=f"Sent from exception_handler (handler_constraints): {error_message}")
            return JSONResponse(
                status_code=settings.app.APP_422_CODE_STATUS,
                content={"detail": exc.errors(), "body": exc.body},
            )

        @app.exception_handler(IntegrityError)
        async def validation_exception_handler_constraints(request, exc: IntegrityError):
            error_message = await errors.get_message(exc)
            logging.log(level=logging.INFO, msg=f"Sent from exception_handler (handler_constraints): {error_message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{error_message}",
            )
