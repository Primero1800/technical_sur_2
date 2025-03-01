from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict


base_username_field = Annotated[str, Field(
        min_length=3, max_length=32,
        default='username',
        title='User name',
        description='The alias of user, that uses in application',
    )]


class UserBase(BaseModel):
    username : base_username_field


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='User id',
        description='The ID of user, that uses in application'
    )]


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserPartialUpdate(UserCreate):
    username: Optional[base_username_field] = None


# class CreateUser(BaseModel):
#     name: Optional[str] = Field(min_length=3, max_length=30, default="John Doe")
#     email: Annotated[
#         EmailStr,
#         Field(
#             title="Email address", description="Valid email address of person, please"
#         ),
#     ]
