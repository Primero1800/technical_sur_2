from fastapi import APIRouter, Depends

from src.api_v1.users.schemas import User, UserCreate
from .dependencies import validate_auth_user, get_current_active_auth_user, get_current_token_payload
from .schemas import TokenInfo
from .utils import jwt_encode


router = APIRouter()


@router.post('/login')
async def auth_user_issue_jwt(
        user: User = Depends(validate_auth_user)
) -> TokenInfo:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
    }
    jwt_access_token = jwt_encode(
        payload=jwt_payload
    )
    return TokenInfo(
        access_token=jwt_access_token
    )


@router.get("/user-jwt-info")
async def auth_user_check_info(
        user: User = Depends(get_current_active_auth_user),
        jwt_payload: dict = Depends(get_current_token_payload)
) -> dict:
    print('UUUUUUUSSSSSSSSSSSSSERRRRR ', user, type(user))
    return {
        'last_login': jwt_payload.get('iat'),
        **user.model_dump(),
    }