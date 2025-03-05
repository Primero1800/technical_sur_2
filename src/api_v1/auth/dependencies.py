from fastapi import Form, Depends
from fastapi.security import (
    HTTPBearer, OAuth2PasswordBearer,
)
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import verify_hash, jwt_decode, jwt_encode
from src.core.config import DBConfigurer
from src.errors import unauthed, unauthorized, bad_request
import src.api_v1.users.crud as users_crud
from ..users.schemas import User
from ...core.settings import settings
from . import validators

HTTP_BEARER = HTTPBearer(auto_error=False)
OAUTH2_SCHEME = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt_auth/login"
)


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
        token: str = Depends(OAUTH2_SCHEME),
) -> dict:
    jwt_payload: dict = {}
    try:
        jwt_payload: dict = jwt_decode(
            token_cred=token,
        )
    except InvalidTokenError as error:
        await bad_request(
            detail=f"Invalid token error: {error}",
            auth_headers='bearer'
        )
    return jwt_payload


async def get_current_user_from_payload_to_operate(
        jwt_payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> User:
    await validators.validate_token_by_type(
        token_type_need=settings.auth_jwt.access_token_type,
        jwt_payload=jwt_payload
    )
    user = await get_current_user_from_payload(
        jwt_payload=jwt_payload,
        session=session
    )
    return user


async def get_current_user_from_payload_to_refresh(
        jwt_payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
) -> User:
    await validators.validate_token_by_type(
        token_type_need=settings.auth_jwt.refresh_token_type,
        jwt_payload=jwt_payload
    )
    user = await get_current_user_from_payload(
        jwt_payload=jwt_payload,
        session=session
    )
    return user


async def get_current_user_from_payload(
        jwt_payload: dict,
        session: AsyncSession
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


# async def get_current_user_from_payload(
#         jwt_payload: dict = Depends(get_current_token_payload),
#         session: AsyncSession = Depends(DBConfigurer.scope_session_dependency)
# ) -> User:
#     user: User
#                             # Проверка, существует ли еще в БД пользователь, извлеченный из токена
#     raw_user_model = await users_crud.get_user(
#         user_id=int(jwt_payload.get('sub')),
#         session=session
#     )
#     print('!!!!!!!!!!!!!!!!!!!!!!!!!! BEFORE USER ', raw_user_model)
#     if user := User(**raw_user_model.to_dict()) if raw_user_model else None:
#         print('!!!!!!!!!!!!!!!!!!!!!!!!!! AFTER USER ', user, type(user))
#         return user
#     await unauthed(
#         detail="Invalid token, user not found",
#         auth_headers='Bearer',
#     )


async def get_current_active_auth_user(
        user: User = Depends(get_current_user_from_payload_to_operate)
) -> User:
    if not user.is_active:
        await unauthorized(
            detail=f"User '{user.username}' is not activated",
            auth_headers='Bearer'
        )
    return user


async def create_jwt_token(
        token_type: str,
        payload: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
) -> str:
    data = {settings.auth_jwt.token_type_field: token_type}
    data.update(payload)
    jwt_access_token = jwt_encode(
        payload=data,
        expire_minutes=expire_minutes
    )
    return jwt_access_token


async def create_access_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
    }
    jwt_access_token = await create_jwt_token(
        token_type=settings.auth_jwt.access_token_type,
        payload=jwt_payload,
    )
    return jwt_access_token


async def create_refresh_token(
    user: User,
) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    jwt_refresh_token = await create_jwt_token(
        token_type=settings.auth_jwt.refresh_token_type,
        payload=jwt_payload,
        expire_minutes=settings.auth_jwt.refresh_token_expire_minutes,
    )
    return jwt_refresh_token
