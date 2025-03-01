from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict


base_title_field = Annotated[str, Field(
        min_length=1, max_length=100,
        default='Title',
        title='Post title',
        description="The post's title",
    )]

base_review_field = Annotated[str, Field(
        max_length=500,
        default='Review',
        title='Post review',
        description="The post's review",
    )]


class PostBase(BaseModel):
    title: base_title_field
    review: base_review_field


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='Post id',
        description='The ID of post, that uses in application'
    )]


class PostCreate(PostBase):
    pass


class PostUpdate(PostCreate):
    pass


class PostPartialUpdate(PostCreate):
    title: Optional[base_title_field] = None
    review: Optional[base_review_field] = None
