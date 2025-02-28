from typing import List

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models import Product
from .schemas import ProductCreate


async def get_products(session: AsyncSession) -> List[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    product: Product | None = await session.get(Product, product_id)
    return product


async def create_product(session: AsyncSession, instance: ProductCreate) -> Product:
    product = Product(**instance.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
