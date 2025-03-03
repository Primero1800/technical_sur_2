from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint

from .base import Base

from .order import Order
from .product import Product


order_product_association_table = Table(
    "order_product_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", ForeignKey(Order.id), nullable=False),
    Column("product_id", ForeignKey(Product.id), nullable=False),
    UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
)
