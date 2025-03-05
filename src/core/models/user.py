from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base

from typing import TYPE_CHECKING, List

# from src.api_v1.auth.utils import DEFAULT_HASH_PASSWORD


if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(
        default='UN',
        server_default='UN',
    )
    email: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True, server_default='True')

    posts: Mapped[List['Post']] = relationship(back_populates="user")
    profile: Mapped['Profile'] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
