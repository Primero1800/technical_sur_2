from fastapi import FastAPI

from src.config.app_config import create_app, get_custom_openapi
from src.config.swagger_config import config_swagger
from src.settings import settings


app = create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = get_custom_openapi(app)
config_swagger(app, settings.app.APP_TITLE)
