from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

base_name_field = Annotated[str, Field(
        min_length=3, max_length=75,
        default='Unknown product',
        title='Product name',
        description='The name of product, that uses in application'
    )]

base_description_field = Annotated[Optional[str], Field(
        max_length=300,
        default='',
        title='Product description',
        description='The description of product, that uses in application'
    )]

base_price_field = Annotated[int, Field(
        # max_digits=6,
        default=100,
        title='Product price',
        description='The price of product, that uses in application'
    )]


class ProductBase(BaseModel):
    name : base_name_field
    description: base_description_field
    price: base_price_field


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='Product id',
        description='The ID of product, that uses in application'
    )]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductPartialUpdate(ProductCreate):
    name: Optional[base_name_field] = None
    description: Optional[base_description_field] = None
    price: Optional[base_price_field] = None
