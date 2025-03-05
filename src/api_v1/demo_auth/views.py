import secrets
import uuid
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request

from src.errors import unauthed, bad_request

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


@router.get('/basic-auth')
async def basic_auth_credentials(
        # credentials: Annotated[HTTPBasicCredentials, Depends(security)]
        request: Request,
        credentials: HTTPBasicCredentials = Depends(security)
):
    return {
        'message': f"Hi {credentials.username}!",
        'detail': f"Your password is '{credentials.password}'. Keep it in secret...",
        # 'request': request.headers
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
        request: Request,
        auth_username: str = Depends(get_auth_user_username)
):
    return {
        'message': f"Hi {auth_username}!",
        'detail': f"Your already logged in",
        # 'request': request.headers
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

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID = 'web-app-cookie-session-id'


async def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post('/login-cookie')
async def demo_auth_login_cookie(
        response: Response,
        auth_username: str = Depends(get_auth_user_username)
):
    session_id = await generate_session_id()
    COOKIES[session_id] = {
        'cooked_username': auth_username,
        'login_at': datetime.now()
    }
    response.set_cookie(COOKIE_SESSION_ID, session_id)
    return {'good': 'boy'}


CustomizedCookie = Cookie(alias=COOKIE_SESSION_ID, default=None, include_in_schema=False)


async def get_session_data(
        session_id: str = CustomizedCookie
) -> dict:
    if session_data := COOKIES.get(session_id):
        return session_data
    await unauthed(
        detail='Not authenticated, no session_data',
        auth_headers=None,
    )


@router.get('/check-login-by-cookie')
async def check_login_by_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    return {
        'result': 'You got session data from cookies',
        **user_session_data,
    }


@router.get('/logout_cookie')
async def logout_cookie(
        response: Response,
        session_id: str = CustomizedCookie,
        user_data: dict = Depends(get_session_data)
):
    try:
        username: dict = user_data['cooked_username']
    except KeyError:
        await bad_request(detail='Invalid user data')

    response.delete_cookie(COOKIE_SESSION_ID)
    # COOKIES.pop(session_id)
    del COOKIES[session_id]
    return {
        'message': f"User '{username}' successfully logged out"
    }



