import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings:
    APP_BASE_DIR = Path(__file__).resolve().parent.parent.parent
    APP_TITLE: str = os.getenv('APP_TITLE')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')

    APP_422_CODE_STATUS: int = int(os.getenv('APP_422_CODE_STATUS'))


class SwaggerSettings:
    pass


class Tags:
    TECH_TAG = os.getenv('TECH_TAG')
    USERS_TAG = os.getenv('USERS_TAG')
    ROOT_TAG = os.getenv('ROOT_TAG')
    SWAGGER_TAG = os.getenv('SWAGGER_TAG')
    PRODUCTS_TAG = os.getenv('PRODUCTS_TAG')


class DB:
    DB_NAME = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
    DB_ENGINE = os.getenv('DB_ENGINE')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    DB_TABLE_PREFIX = os.getenv('DB_TABLE_PREFIX')

    DB_ECHO_MODE = True if os.getenv('DB_ECHO_MODE') == 'True' else False


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()
    db: DB = DB()


settings = Settings()
