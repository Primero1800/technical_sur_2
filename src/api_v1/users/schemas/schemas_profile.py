from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict


base_firstname_field = Annotated[str, Field(
        min_length=1, max_length=50,
        default='John',
        title='User firstname',
        description="The user's firstname",
    )]

base_lastname_field = Annotated[str, Field(
        min_length=1, max_length=50,
        default='Doe',
        title='User lastname',
        description="The user's lastname",
    )]

base_bio_field = Annotated[str, Field(
        min_length=3, max_length=500,
        default='',
        title='User bio',
        description='The bio of user',
    )]


class ProfileBase(BaseModel):
    firstname : base_firstname_field
    lastname: base_lastname_field
    bio: base_bio_field


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='Profile id',
        description='The ID of profile, that uses in application'
    )]


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileCreate):
    pass


class ProfilePartialUpdate(ProfileCreate):
    firstname: Optional[base_firstname_field] = None
    lastname: Optional[base_lastname_field] = None
    bio: Optional[base_bio_field] = None
