from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud as crud
from .schemas import Product, ProductCreate
from src.core.config import DBConfigurer

router = APIRouter()


@router.get('/', response_model=List[Product])
async def get_products(
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> List[Product]:
    return await crud.get_products(session=session)


@router.get('/{product_id}/', response_model=Product)
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Product with id={product_id} not found'
        )
    return product


@router.post('/', response_model=Product)
async def create_product(
        instance: ProductCreate,
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> Product | None:
    return await crud.create_product(session=session, instance=instance)


