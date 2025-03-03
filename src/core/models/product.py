from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.core.models import Base
from ..config.db_config import DBConfigurerInitializer

if TYPE_CHECKING:
    from .order import Order
    from .order_product_association import OrderProductAssociation


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list['Order']] = relationship(
        secondary=DBConfigurerInitializer.utils.camel2snake('OrderProductAssociation'),
        back_populates="products",
    )
    orders_details: Mapped[list['OrderProductAssociation']] = relationship(
        back_populates='product',
        overlaps="orders",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, price={self.price})"

    def __repr__(self):
        return str(self)