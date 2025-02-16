from fastapi import APIRouter, Depends

from app.web_api.dependencies.permission import PermissionDependency, AllowAll
from app.web_api.routes.public.auth import auth_router
from app.web_api.routes.public.health import health_router
from app.web_api.routes.public.presentation import presentation_router

public_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(PermissionDependency([AllowAll]))]
)
public_router.include_router(health_router)
public_router.include_router(auth_router)
public_router.include_router(presentation_router)
