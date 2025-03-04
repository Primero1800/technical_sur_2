import bcrypt
import jwt

from src.core.settings import settings


def jwt_encode(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )


def jwt_decode(
        token_cred: str | bytes,
        public_key: str = settings.auth_jwt.public_key.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(
        jwt=token_cred,
        key=public_key,
        algorithms=[algorithm,],
    )


def get_hash(password: str) -> bytes:
    return bcrypt.hashpw(
        password=password.encode(),
        salt=bcrypt.gensalt(),
    )


def verify_hash(password: str, hash_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hash_password)