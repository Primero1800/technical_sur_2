from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from .user import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_id_nullable: bool = False

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey(User.id),
            nullable=cls._user_id_nullable,
            unique=cls._user_id_unique
        )

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship('User', back_populates=cls._user_back_populates)
