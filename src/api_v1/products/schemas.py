from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name : Annotated[str, Field(
        min_length=3, max_length=75,
        default='Unknown product',
        title='Product name',
        description='The name of product, that uses in application'
    )]
    description: Annotated[Optional[str], Field(
        min_length=300,
        default='',
        title='Product description',
        description='The description of product, that uses in application'
    )]
    price: Annotated[int, Field(
        max_digits=6,
        default=100,
        title='Product price',
        description='The price of product, that uses in application'
    )]


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='Product id',
        description='The ID of product, that uses in application'
    )]


class ProductCreate(ProductBase):
    pass