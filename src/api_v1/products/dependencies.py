from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.config import DBConfigurer
from src.core.models import Product
from . import crud


async def product_by_id(
        product_id: Annotated[int, Path],
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Product with id={product_id} not found'
        )
    return product
