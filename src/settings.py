import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).parent


class AppSettings:
    APP_TITLE: str = os.getenv('APP_TITLE')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')

    APP_422_CODE_STATUS: int = int(os.getenv('APP_422_CODE_STATUS'))


class SwaggerSettings:
    pass


class Tags:
    TECH_TAG = os.getenv('TECH_TAG')
    ROOT_TAG = os.getenv('ROOT_TAG')
    SWAGGER_TAG = os.getenv('SWAGGER_TAG')


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()


settings = Settings()
