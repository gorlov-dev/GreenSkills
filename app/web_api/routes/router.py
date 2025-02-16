from fastapi import APIRouter

from app.web_api.routes.public.router import public_router
from app.web_api.routes.protected.router import protected_router


router = APIRouter()
router.include_router(public_router)
router.include_router(protected_router)
