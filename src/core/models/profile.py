from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base

from .mixin import UserRelationMixin


class Profile(UserRelationMixin, Base):

    _user_id_nullable = False
    _user_id_unique = True
    _user_back_populates = 'profile'

    firstname: Mapped[str] = mapped_column(
        String(50), default="", server_default=""
    )
    lastname: Mapped[str] = mapped_column(
        String(50), default="", server_default=""
    )
    bio: Mapped[str | None] = mapped_column(
        Text, default='', server_default=''
    )

    def __str__(self):
        return f"{self.__class__.__name__}(firstname={self.firstname}, lastname={self.lastname}, bio={self.bio:10})"

    def __repr__(self):
        return str(self)
