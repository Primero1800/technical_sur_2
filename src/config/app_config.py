from typing import Callable, Dict, Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from src.settings import settings


def create_app(docs_url, redoc_url) -> FastAPI:
    app = FastAPI(
        docs_url=docs_url,
        redoc_url=redoc_url,
        # openapi_tags=tags_metadata,
    )
    return app


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


def config_validation_exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        return JSONResponse(
            status_code=settings.app.APP_422_CODE_STATUS,
            content={"detail": exc.errors(), "body": exc.body},
        )
