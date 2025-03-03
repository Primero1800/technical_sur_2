from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base

from .order import Order
from .product import Product
from ..config.db_config import DBConfigurerInitializer


class OrderProductAssociation(Base):
    def __init__(self):
        super().__init__()
        self.__class__.__tablename__ = DBConfigurerInitializer.utils.camel2snake(self.__class__.__name__)

    # __tablename__ = DBConfigurerInitializer.utils.camel2snake('OrderProductAssociation')

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
    )

    @classmethod
    def _get_name(cls):
        return cls.__name__

    order_id: Mapped[int] = mapped_column(ForeignKey(Order.id))
    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id))


# order_product_association_table = Table(
#     "order_product_association",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey(Order.id), nullable=False),
#     Column("product_id", ForeignKey(Product.id), nullable=False),
#     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
# )
