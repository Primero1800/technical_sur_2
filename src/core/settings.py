import os
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AppSettings:
    APP_BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    APP_TITLE: str = os.getenv('APP_TITLE')
    APP_VERSION: str = os.getenv('APP_VERSION')
    APP_DESCRIPTION: str = os.getenv('APP_DESCRIPTION')
    APP_HOST: str = os.getenv('APP_HOST')
    APP_PORT: int = int(os.getenv('APP_PORT'))

    API_PREFIX: str = os.getenv('API_PREFIX')
    API_V1_PREFIX = API_PREFIX + os.getenv('API_V1_PREFIX')

    APP_422_CODE_STATUS: int = int(os.getenv('APP_422_CODE_STATUS'))


class SwaggerSettings:
    pass


class GunicornSettings(BaseSettings):
    WORKERS: int = int(os.getenv('GUNICORN_WORKERS'))
    TIMEOUT: int = int(os.getenv('GUNICORN_TIMEOUT'))


class Tags(BaseSettings):
    TECH_TAG: str = os.getenv('TECH_TAG')
    USERS_TAG: str = os.getenv('USERS_TAG')
    ROOT_TAG: str = os.getenv('ROOT_TAG')
    SWAGGER_TAG: str = os.getenv('SWAGGER_TAG')
    PRODUCTS_TAG: str = os.getenv('PRODUCTS_TAG')
    AUTH_TAG: str = os.getenv('AUTH_TAG')
    JWT_AUTH_TAG: str = os.getenv('JWT_AUTH_TAG')


class DB(BaseSettings):

    DB_NAME: str = os.getenv('DB_NAME_TEST') if 'pytest' in sys.modules else os.getenv('DB_NAME')
    DB_ENGINE: str = os.getenv('DB_ENGINE')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))

    DB_TABLE_PREFIX: str = os.getenv('DB_TABLE_PREFIX')

    DB_ECHO_MODE: bool = True if os.getenv('DB_ECHO_MODE') == 'True' else False

    DB_URL: str = ''


class LoggingConfig(BaseSettings):
    LOGGING_LEVEL: Literal['debug', 'info', 'warning', 'error', 'critical'] = os.getenv('LOGGING_LEVEL')
    LOGGING_FORMAT: str = os.getenv('LOGGING_FORMAT')


class AuthJWT:
    private_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-private.pem"
    public_key = AppSettings.APP_BASE_DIR / "src" / "core" / "config"/"certs"/"jwt-public.pem"
    algorithm = os.getenv('JWT_ALGORYTHM')
    token_type_field = os.getenv('TOKEN_TYPE_FIELD')
    access_token_expire_minutes = float(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    refresh_token_expire_minutes = float(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))
    access_token_type = os.getenv('ACCESS_TOKEN_TYPE')
    refresh_token_type = os.getenv('REFRESH_TOKEN_TYPE')
    default_password = os.getenv('DEFAULT_PASSWORD')


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    tags: Tags = Tags()
    db: DB = DB()
    auth_jwt: AuthJWT = AuthJWT()
    gunicorn: GunicornSettings = GunicornSettings()
    logging: LoggingConfig = LoggingConfig()


settings = Settings()


def get_db_connection():
    return '{}://{}:{}@{}:{}/{}'.format(
        settings.db.DB_ENGINE,
        settings.db.DB_USER,
        settings.db.DB_PASSWORD,
        settings.db.DB_HOST,
        settings.db.DB_PORT,
        settings.db.DB_NAME,
    )


settings.db.DB_URL = get_db_connection()
