import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

router = APIRouter()
security = HTTPBasic()


username_to_passwords = {
    'admin': 'admin',
    'primero': '12345678',
}

token_to_username = {
    '2e756e5563f0be1c7a25f3c1b59580eaf23c06323919580921082290b2c414f9': 'primero',
    '0228e11bf2b867c817927547c25fb99c1dbe08090bd37c5bfb290c4499cb4b89': 'admin',
}


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


@router.get('/basic-auth')
async def basic_auth_credentials(
        # credentials: Annotated[HTTPBasicCredentials, Depends(security)]
        credentials: HTTPBasicCredentials = Depends(security)
):
    return {
        'message': f"Hi {credentials.username}!",
        'detail': f"Your password is '{credentials.password}'. Keep it in secret..."
    }


async def get_auth_user_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = username_to_passwords.get(credentials.username)
    if not correct_password:
        await unauthed()
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        correct_password.encode('utf-8')
    ):
        await unauthed()
    return credentials.username


@router.get('/basic-auth-username')
async def basic_auth_username(
        # credentials: Annotated[HTTPBasicCredentials, Depends(security)]
        auth_username: str = Depends(get_auth_user_username)
):
    return {
        'message': f"Hi {auth_username}!",
        'detail': f"Your already logged in"
    }


async def get_username_by_static_auth_token(
        auth_token: str = Header(alias='x-auth-token')
) -> str:
    if username := token_to_username.get(auth_token):
        return username
    # await bad_request()
    await unauthed(
        detail='Invalid token',
        auth_headers=None
    )


@router.get('/some-http-header-auth')
async def demo_auth_some_http_header(
        username: str = Depends(get_username_by_static_auth_token)
):
    return {
        'message': f"Hi {username}!",
        'detail': f"Your already logged in"
    }


