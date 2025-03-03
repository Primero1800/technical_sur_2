import re
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session,
)

from sqlalchemy.exc import IntegrityError

from src.core.settings import settings


class Utils:
    prefix = settings.db.DB_TABLE_PREFIX

    @staticmethod
    def db_tablename_camel(cls):
        return ''.join(s.capitalize() for s in re.split(r'[ _-]', cls.__name__.lower()))

    @staticmethod
    def camel2snake(name):
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return Utils.prefix + '_' + snake.lower()


class DBConfigurerInitializer:
    utils = Utils()

    def __init__(self):
        self.connection_path = settings.db.DB_URL
        self.engine = create_async_engine(self.connection_path, echo=settings.db.DB_ECHO_MODE)
        self.Session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.Session,
            scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.Session() as session:
            yield session
            await session.close()

    async def scope_session_dependency(self):
        session = self.get_scoped_session()
        yield session
        await session.close()


DBConfigurer = DBConfigurerInitializer()
