from fastapi import APIRouter, Request, HTTPException, Response
from pydantic import BaseModel, Field

from app.use_cases.auth.login import AuthUseCaseLoginContext, AuthUseCaseLogin
from app.use_cases.user.create import UserUseCaseCreateContext, UserUseCaseCreate
from app.web_api.schemas.user import UserResponse
from app.web_api.utils.token_helper import TokenHelper

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])


#########################################################################################
# Регистрация пользователя
class AuthRequestRegister(UserUseCaseCreateContext):
    pass


@auth_router.post("/register", response_model=UserResponse)
async def route_release(request: Request, payload: AuthRequestRegister):
    try:
        return await UserUseCaseCreate().execute(payload)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


#########################################################################################
# Авторизация пользователя
class AuthRequestLogin(AuthUseCaseLoginContext):
    pass


class AuthResponseLogin(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


@auth_router.post("/login", response_model=AuthResponseLogin)
async def route_release(request: Request, payload: AuthRequestLogin):
    try:
        user = await AuthUseCaseLogin().execute(payload)

        return {
            "token": TokenHelper.encode(payload={"user_id": user.id}),
            "refresh_token": TokenHelper.encode(payload={"sub": "refresh"})
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
