from fastapi import APIRouter, Depends, HTTPException, Request

from app.use_cases.user.read import UserUseCaseRead
from app.web_api.schemas.user import UserResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


#########################################################################################
#
@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(
    request: Request,
    use_case: UserUseCaseRead = Depends(),
):
    """
    Получение информации о текущем пользователе.
    """
    user_id = request.user.id  # Получаем ID пользователя из авторизации

    user = await use_case.execute(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return UserResponse.model_validate(user)
