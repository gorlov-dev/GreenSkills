from fastapi import APIRouter, Depends

from app.web_api.dependencies.permission import IsAuthenticated, PermissionDependency

from app.web_api.routes.protected.auth import auth_router
from app.web_api.routes.protected.presentation import presentation_router
from app.web_api.routes.protected.slide_template import template_router
from app.web_api.routes.protected.slide import slide_router
from app.web_api.routes.protected.rag import rag_router

protected_router = APIRouter(
    prefix="/api/v1", dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
protected_router.include_router(auth_router)
protected_router.include_router(presentation_router)
protected_router.include_router(template_router)
protected_router.include_router(slide_router)
protected_router.include_router(rag_router)
