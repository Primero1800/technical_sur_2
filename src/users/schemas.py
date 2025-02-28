from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr


class CreateUser(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=30, default="John Doe")
    email: Annotated[
        EmailStr,
        Field(
            title="Email address", description="Valid email address of person, please"
        ),
    ]
