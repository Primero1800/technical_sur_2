from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api_v1.users import crud
from .dependencies import user_by_id
from .schemas import User, UserCreate, UserUpdate, UserPartialUpdate
from src.core.config import DBConfigurer

router = APIRouter()


@router.get('/', response_model=List[User])
async def get_users(
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> List[User]:
    return await crud.get_users(session=session)


@router.get('/{user_id}/', response_model=User)
async def get_user(
        user: User = Depends(user_by_id)
) -> User:
    return user


@router.post(
    '/',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        instance: UserCreate,
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> User | None:
    return await crud.create_user(session=session, instance=instance)


@router.put('/{user_id}/', response_model=User)
async def update_user(
        instance: UserUpdate,
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency),
) -> User:
    user = await crud.update_user(
        session=session,
        user=user,
        instance=instance
    )
    return user


@router.patch('/{user_id}/', response_model=User)
async def update_user(
        instance: UserPartialUpdate,
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency),
) -> User:
    user = await crud.update_user(
        session=session,
        user=user,
        instance=instance,
        is_partial=True,
    )
    return user


@router.delete(
    '/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        user: User = Depends(user_by_id),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> None:
    await crud.delete_user(
        session=session,
        user=user
    )

