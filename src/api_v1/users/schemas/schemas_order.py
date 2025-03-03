from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


base_promocode_field = Annotated[str | None, Field(
        min_length=1, max_length=100,
        default='Promocode',
        title='Order promocode',
        description="The order's promocode",
    )]


class OrderBase(BaseModel):
    promocode: base_promocode_field


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(
        title='Order id',
        description='The ID of order, that uses in application'
    )]
    created_at: Annotated[datetime | None, Field(
        title='Order created at',
        description="The order's time of creation",
    )]


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderCreate):
    pass


class OrderPartialUpdate(OrderCreate):
    promocode: Optional[base_promocode_field] = None
