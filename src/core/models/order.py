from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from ..config.db_config import DBConfigurerInitializer

if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    products: Mapped[list['Product']] = relationship(
        secondary=DBConfigurerInitializer.utils.camel2snake('OrderProductAssociation'),
        back_populates="orders",
        overlaps="orders_details",
    )
    products_details: Mapped[list['OrderProductAssociation']] = relationship(
        back_populates='order',
        overlaps="orders, products",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, created_at={self.created_at})"

    def __repr__(self):
        return str(self)
