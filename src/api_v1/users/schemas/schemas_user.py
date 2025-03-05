from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict


base_username_field = Annotated[str, Field(
        min_length=3, max_length=32,
        default='username',
        title='User name',
        description='The alias of user, that uses in application',
    )]

base_password_field = Annotated[str, Field(
        min_length=8,
        default='password',
        title='Hashed password',
        description='The alias of user hashed password, that uses in application'
    )]

base_email_field = Annotated[EmailStr | None, Field(
        min_length=3, max_length=32,
        default=None,
        title='User email',
        description='The alias of user email, that uses in application',
    )]


class UserBase(BaseModel):
    username: base_username_field
    email: Optional[base_email_field] = None
    password: base_password_field


class User(UserBase):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: Annotated[int, Field(
        title='User id',
        description='The ID of user, that uses in application'
    )]
    is_active: Annotated[bool, Field(
        title='User is_active flag',
        description="The flag of user's activity",
        default=True,
    )]


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserPartialUpdate(UserCreate):
    username: Optional[base_username_field] = None
    email: Optional[base_email_field] = None
    password: Optional[base_password_field] = None
