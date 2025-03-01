from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[List['Post']] = relationship(back_populates="user")