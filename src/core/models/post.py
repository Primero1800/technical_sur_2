from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base

from .mixin import UserRelationMixin


class Post(UserRelationMixin, Base):

    _user_id_nullable = False
    _user_id_unique = False
    _user_back_populates = 'posts'

    title: Mapped[str] = mapped_column(
        String(100), unique=False
    )
    review: Mapped[str] = mapped_column(
        Text, default="", server_default=""
    )

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title}, review={self.review:20})"

    def __repr__(self):
        return str(self)
