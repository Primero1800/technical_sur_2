from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html, get_redoc_html
)
from starlette import status
from src.settings import settings


def config_swagger(app: FastAPI, app_title='Unknown application'):
    @app.get('/docs', status_code=status.HTTP_200_OK, include_in_schema=False)
    @app.get('/docs/', status_code=status.HTTP_200_OK, tags=[settings.tags.SWAGGER_TAG])
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app_title + ' Swagger UI',
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )


    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


    @app.get("/redoc", include_in_schema=False)
    @app.get("/redoc/", status_code=status.HTTP_200_OK, tags=[settings.tags.SWAGGER_TAG])
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )