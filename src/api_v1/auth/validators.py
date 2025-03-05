from src.core.settings import settings
from src.errors import unauthed


async def validate_token_by_type(
        token_type_need: str,
        jwt_payload: dict,
) -> bool:
    # Проверка типа токена в запросе. Если не 'refresh', то кидаем ошибку
    token_type: str = jwt_payload.get(settings.auth_jwt.token_type_field)
    if token_type != token_type_need:
        await unauthed(
            detail=f"Incorrect token type: need {token_type_need!r}, "
                   f"got {token_type!r}",
            auth_headers='Bearer',
        )
    return True