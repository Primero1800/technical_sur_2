from pydantic import BaseModel

from src.core.settings import settings


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
