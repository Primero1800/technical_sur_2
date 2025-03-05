from fastapi import Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import verify_hash, jwt_decode
from src.core.config import DBConfigurer
from src.errors import unauthed, unauthorized, bad_request
import src.api_v1.users.crud as users_crud
from ..users.schemas import User

HTTP_BEARER = HTTPBearer(auto_error=False)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
):
    user: User
    raw_user_model = await users_crud.get_user_by_username(
        session=session,
        username=username,
    )
    if not (  # Проверка, существует ли пользователь в БД
            user := User(**raw_user_model.to_dict()) if raw_user_model else None
    ):
        await unauthed(
            auth_headers='Bearer'
        )
    if not verify_hash(  # Проверка валидности пароля по функции хэширования
            password=password,
            hash_password=user.password.encode()
    ):
        await unauthed(
            auth_headers='Bearer'
        )
    if not user.is_active:  # Проверка, активирован ли пользователь
        await unauthorized(
            detail=f"User '{user.username}' is not activated",
            auth_headers='Bearer'
        )
    return user


async def get_current_token_payload(
        token_creds: str | HTTPAuthorizationCredentials = Depends(HTTP_BEARER),
) -> dict:

    if isinstance(token_creds, HTTPAuthorizationCredentials):
        token_creds = token_creds.credentials
    try:
        jwt_payload: dict = jwt_decode(
            token_cred=token_creds,
        )
    except InvalidTokenError as error:
        await bad_request(
            detail=f"Invalid token error: {error}",
            auth_headers='bearer'
        )
    return jwt_payload


async def get_current_user_from_payload(
        jwt_payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> User:
    user: User
                            # Проверка, существует ли еще в БД пользователь, извлеченный из токена
    raw_user_model = await users_crud.get_user(
        user_id=int(jwt_payload.get('sub')),
        session=session
    )
    if user := User(**raw_user_model.to_dict()) if raw_user_model else None:
        return user
    await unauthed(
        detail="Invalid token, user not found",
        auth_headers='Bearer',
    )


async def get_current_active_auth_user(
        user: User = Depends(get_current_user_from_payload)
) -> User:
    if not user.is_active:
        await unauthorized(
            detail=f"User '{user.username}' is not activated",
            auth_headers='Bearer'
        )
    return user
