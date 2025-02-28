from fastapi import APIRouter

from .products.views import router as products_router
from src.core.settings import settings

router = APIRouter()
router.include_router(
    products_router,
    prefix="/products",
    tags=[
        settings.tags.PRODUCTS_TAG,
    ]
)