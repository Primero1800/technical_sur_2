from fastapi import APIRouter

from .products.views import router as products_router
from .users.views import router as users_router
from .demo_auth.views import router as auth_router
from .auth.views import router as jwt_router
from src.core.settings import settings

router = APIRouter()

router.include_router(
    auth_router,
    prefix="/demo-auth",
    tags=[
        settings.tags.AUTH_TAG,
    ]
)

router.include_router(
    users_router,
    prefix="/users",
    tags=[
        settings.tags.USERS_TAG,
    ]
)

router.include_router(
    jwt_router,
    prefix="/jwt_auth",
    tags=[
        settings.tags.JWT_AUTH_TAG,
    ]
)

router.include_router(
    products_router,
    prefix="/products",
    tags=[
        settings.tags.PRODUCTS_TAG,
    ]
)