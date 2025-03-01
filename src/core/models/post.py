from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base

from .user import User


class Post(Base):
    title: Mapped[str] = mapped_column(
        String(100), unique=False
    )
    review: Mapped[str] = mapped_column(
        Text, default="", server_default=""
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id), nullable=False,
    )
    user: Mapped['User'] = relationship(back_populates="posts")