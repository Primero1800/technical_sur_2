from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.config import DBConfigurer
from src.core.models import User
from . import crud


async def user_by_id(
        user_id: Annotated[int, Path],
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> User:
    user = await crud.get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id={user_id} not found'
        )
    return user
