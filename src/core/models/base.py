from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from src.core.settings import settings


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return '_'.join([settings.db.DB_TABLE_PREFIX, cls.__name__.lower()])

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
