from fastapi import APIRouter, Response

health_router = APIRouter(prefix='/health', tags=['Health'])


@health_router.get("")
async def health_app():
    return Response(status_code=200)
