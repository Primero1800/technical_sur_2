from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)