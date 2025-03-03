from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base

from .order import Order
from .product import Product
from ..config.db_config import DBConfigurerInitializer


class OrderProductAssociation(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.__tablename__ = DBConfigurerInitializer.utils.camel2snake(self.__class__.__name__)

    # __tablename__ = DBConfigurerInitializer.utils.camel2snake('OrderProductAssociation')
    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey(Order.id))
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id))
    count: Mapped[int] = mapped_column(default=1, server_default=str(1))
    item_price: Mapped[int] = mapped_column(default=0, server_default=str(0))

    order: Mapped[List['Order']] = relationship(
        back_populates="products_details",
        overlaps="orders, products"
    )
    product: Mapped[List['Product']] = relationship(
        back_populates="orders_details",
        overlaps="orders, products"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, product_id={self.product_id}, order_id={self.order_id}, count={self.count})"

    def __repr__(self):
        return str(self)


# order_product_association_table = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey(Order.id), nullable=False),
#     Column("product_id", ForeignKey(Product.id), nullable=False),
#     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
# )
