import datetime

from fastapi import APIRouter, Depends

from src.api_v1.users.schemas import User, UserCreate
from . import dependencies as deps
from .schemas import TokenInfo


router = APIRouter(dependencies=[Depends(deps.HTTP_BEARER)])


@router.post('/login')
async def auth_user_issue_jwt(
        user: User = Depends(deps.validate_auth_user)
) -> TokenInfo:

    access_token = await deps.create_access_token(user)
    refresh_token = await deps.create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/user-jwt-info")
async def auth_user_check_info(
        user: User = Depends(deps.get_current_active_auth_user),
        jwt_payload: dict = Depends(deps.get_current_token_payload)
) -> dict:
    return {
        'last_login': datetime.datetime.fromtimestamp(
            timestamp=jwt_payload.get('iat'),
            tz=datetime.timezone.utc
        ),
        **user.model_dump(),
    }


@router.get("/token-jwt-info")
async def get_current_jwt_token_from_headers(
        token: str = Depends(deps.OAUTH2_SCHEME),
        jwt_payload: dict = Depends(deps.get_current_token_payload)
) -> dict:
    return {'token': token, **jwt_payload}
