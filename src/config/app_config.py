from typing import Callable, Dict, Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
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
