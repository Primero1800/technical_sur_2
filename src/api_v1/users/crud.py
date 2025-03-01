from typing import List
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserUpdate, UserCreate, UserPartialUpdate

from src.core.models import User


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    user: User | None = await session.get(User, user_id)
    return user


async def create_user(session: AsyncSession, instance: UserCreate) -> User:
    user = User(**instance.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user: User,
        instance: UserUpdate | UserPartialUpdate,
        is_partial: bool = False
) -> User:
    for key, val in instance.model_dump(
        exclude_unset=is_partial
    ).items():
        setattr(user, key, val)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(
        session: AsyncSession, user: User
) -> None:
    await session.delete(user)
    await session.commit()
