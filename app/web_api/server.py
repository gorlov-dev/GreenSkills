from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from app.web_api.middleware.auth_backend import AuthBackend
from app.web_api.routes.router import router
from app.web_api.routes.websocket.router import ws_router
from starlette.requests import HTTPConnection


def on_auth_error(conn: HTTPConnection, exc: Exception) -> Response:
    return JSONResponse(
        status_code=401,
        content={"error": str(exc)},
    )


middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(AuthenticationMiddleware, backend=AuthBackend(), on_error=on_auth_error),
]


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Евстигней",
        description="Евстигней - ваш личный помощник в подготовке презентаций",
        version="1.0.0",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json",
        middleware=middlewares,
    )

    app_.include_router(router)
    app_.include_router(ws_router)
    return app_


app = create_app()
