from fastapi import APIRouter, HTTPException, Request

from app.use_cases.presentation.read import PresentationUseCaseRead
from app.use_cases.slide.create import SlideUseCaseCreate, SlideUseCaseCreateContext
from app.use_cases.slide.delete import SlideUseCaseDelete, SlideUseCaseDeleteContext
from app.use_cases.slide.read import SlideUseCaseRead
from app.use_cases.slide.update import SlideUseCaseUpdate, SlideUseCaseUpdateContext
from app.web_api.schemas.slide import (
    SlideCreateRequest,
    SlideResponse,
    SlideUpdateRequest,
)

slide_router = APIRouter(prefix="/slide", tags=["Slide"])


#########################################################################################
#
@slide_router.post("/", response_model=SlideResponse)
async def create_slide(
    request: Request,
    payload: SlideCreateRequest,
):
    """
    Создание нового слайда.
    """
    user_id = request.user.id  # Получаем ID владельца из запроса

    try:
        context = SlideUseCaseCreateContext(
            user_id=user_id,
            template_id=payload.template_id,
            presentation_id=payload.presentation_id,
            prompt=payload.prompt,
            position=payload.position,
            data=payload.data,
        )
        slide = await SlideUseCaseCreate().execute(context)
        return SlideResponse.model_validate(slide)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#########################################################################################
#
@slide_router.put("/{entity_id}", response_model=SlideResponse)
async def update_slide(
    entity_id: int,
    request: Request,
    payload: SlideUpdateRequest,
):
    """
    Обновление данных слайда.
    """
    user_id = request.user.id  # Получаем ID пользователя из запроса

    try:
        # Вызываем use-case для обновления данных слайда
        context = SlideUseCaseUpdateContext(
            slide_id=entity_id,
            user_id=user_id,
            template_id=payload.template_id,
            data=payload.data,
            prompt=payload.prompt,
        )

        updated_slide = await SlideUseCaseUpdate().execute(context)

        return updated_slide
    except PermissionError:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#########################################################################################
#
@slide_router.delete("/{entity_id}")
async def delete_slide(
    entity_id: int,
    request: Request,
):
    """
    Удаление слайда по ID.
    """
    user_id = request.user.id  # Получаем ID владельца из запроса

    try:
        context = SlideUseCaseDeleteContext(user_id=user_id, slide_id=entity_id)

        await SlideUseCaseDelete().execute(context)

        return {"message": "Слайд успешно удалён"}
    except PermissionError:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
