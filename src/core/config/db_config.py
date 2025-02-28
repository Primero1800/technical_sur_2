from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.models import Base
from sqlalchemy.exc import IntegrityError

from src.core.settings import settings


def get_db_connection():
    return '{}://{}:{}@{}:{}/{}'.format(
        settings.db.DB_ENGINE,
        settings.db.DB_USER,
        settings.db.DB_PASSWORD,
        settings.db.DB_HOST,
        settings.db.DB_PORT,
        settings.db.DB_NAME,
    )


class DBConfigurerInitializer:
    def __init__(self):
        self.connection_path = get_db_connection()
        self.engine = create_async_engine(self.connection_path, echo=settings.db.DB_ECHO_MODE)
        self.Session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,

        )


DBConfigurer = DBConfigurerInitializer()
