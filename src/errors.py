from fastapi import HTTPException
from starlette import status


async def unauthed(
        detail="Incorrect username or password",
        auth_headers: str | None = 'Basic'
):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": auth_headers} if auth_headers else None,
    )


async def bad_request(
        detail='Bad request',
        auth_headers: str = 'Token'
):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        headers={'WWW-Authenticate': auth_headers},
    )


async def unauthorized(
        detail='User not authorized',
        auth_headers: str = 'Token'
):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
        headers={'WWW-Authenticate': auth_headers},
    )