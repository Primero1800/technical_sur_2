from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud as crud
from .dependencies import product_by_id
from .schemas import Product, ProductCreate, ProductUpdate, ProductPartialUpdate
from src.core.config import DBConfigurer

router = APIRouter()


@router.get('/', response_model=List[Product])
async def get_products(
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> List[Product]:
    return await crud.get_products(session=session)


@router.get('/{product_id}/', response_model=Product)
async def get_product(
        product: Product = Depends(product_by_id)
) -> Product:
    return product


@router.post(
    '/',
    response_model=Product,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
        instance: ProductCreate,
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> Product | None:
    return await crud.create_product(session=session, instance=instance)


@router.put('/{product_id}/', response_model=Product)
async def update_product(
        instance: ProductUpdate,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency),
) -> Product:
    product = await crud.update_product(
        session=session,
        product=product,
        instance=instance
    )
    return product


@router.patch('/{product_id}/', response_model=Product)
async def update_product(
        instance: ProductPartialUpdate,
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency),
) -> Product:
    product = await crud.update_product(
        session=session,
        product=product,
        instance=instance,
        is_partial=True,
    )
    return product


@router.delete(
    '/{product_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
        product: Product = Depends(product_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> None:
    await crud.delete_product(
        session=session,
        product=product
    )

