from typing import List
from fastapi import APIRouter, HTTPException, Request
from fastapi.param_functions import Query

from app.use_cases.presentation.delete import (
    PresentationUseCaseDelete,
    PresentationUseCaseDeleteContext,
)
from app.use_cases.presentation.generate_fake import (
    PresentationUseCaseGenerateFake,
    PresentationUseCaseGenerateFakeContext,
)
from app.use_cases.presentation.publish import (
    PresentationUseCasePublish,
    PresentationUseCasePublishContext,
)
from app.use_cases.presentation.read import PresentationUseCaseRead
from app.use_cases.presentation.read_list import (
    PresentationUseCaseList,
    PresentationUseCaseListContext,
)
from app.use_cases.slide.read import SlideUseCaseRead
from app.use_cases.presentation.reorder import (
    PresentationUseCaseSlidesReorder,
    PresentationUseCaseSlidesReorderContext,
)
from app.web_api.schemas.presentation import (
    PresentationReorderSlideRequest,
    PresentationResponse,
    PresentationGenerateRequest,
)

presentation_router = APIRouter(prefix="/presentation", tags=["Presentation"])


#########################################################################################
#
@presentation_router.get("/", response_model=List[PresentationResponse])
async def list_presentations(
    request: Request,
    sort_by: str = Query(default="updated_at", description="Поле для сортировки"),
    sort_order: str = Query(
        default="desc", description="Порядок сортировки (asc/desc)"
    ),
):
    """
    Получение списка презентаций текущего пользователя.
    """
    user_id = request.user.id  # Получаем ID пользователя из авторизации

    try:
        context = PresentationUseCaseListContext(
            user_id=user_id, sort_by=sort_by, sort_order=sort_order
        )
        presentations = await PresentationUseCaseList().execute(context)
        return [PresentationResponse.model_validate(p) for p in presentations]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#########################################################################################
#
@presentation_router.get("/{entity_id}", response_model=PresentationResponse)
async def get_by_id(entity_id: int):
    entity = await PresentationUseCaseRead().execute(entity_id)

    if entity is None:
        raise HTTPException(status_code=404, detail="Не найдено")
    return PresentationResponse.model_validate(entity)


#########################################################################################
#
@presentation_router.post("/generate", response_model=PresentationResponse)
async def generate_presentation(
    request: Request,
    payload: PresentationGenerateRequest,
):
    """
    Генерация презентации на основе запроса.
    """
    try:
        context = PresentationUseCaseGenerateFakeContext(
            owner_id=request.user.id,
            prompt=payload.prompt,
            slides_count=payload.slides_count,
        )
        presentation = await PresentationUseCaseGenerateFake().execute(context)
        return PresentationResponse.model_validate(presentation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#########################################################################################
#
@presentation_router.post(
    "/{entity_id}/reorder-slides", response_model=PresentationResponse
)
async def reorder_slide(
    entity_id: int,
    request: Request,
    payload: PresentationReorderSlideRequest,
):
    """
    Изменение порядка слайда в презентации.
    """
    user_id = request.user.id  # Получаем ID владельца из запроса

    # Проверяем, существует ли презентация
    presentation = await PresentationUseCaseRead().execute(entity_id)
    if presentation is None:
        raise HTTPException(status_code=404, detail="Презентация не найдена")

    # Проверяем, существует ли слайд
    slide = await SlideUseCaseRead().execute(payload.slide_id)
    if slide is None or slide.presentation_id != entity_id:
        raise HTTPException(status_code=404, detail="Слайд не найден")

    # Проверяем, является ли пользователь владельцем презентации
    if presentation.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    # Вызываем use-case для смены порядка
    context = PresentationUseCaseSlidesReorderContext(
        slide_id=payload.slide_id,
        position=payload.position,
        owner_id=user_id,
    )
    presentation = await PresentationUseCaseSlidesReorder().execute(context)

    return presentation


#########################################################################################
#
@presentation_router.delete("/{entity_id}")
async def delete_presentation(
    entity_id: int,
    request: Request,
):
    """
    Удаление презентации по ID.
    """
    user_id = request.user.id  # Получаем ID владельца из запроса

    try:
        context = PresentationUseCaseDeleteContext(
            user_id=user_id, presentation_id=entity_id
        )

        await PresentationUseCaseDelete().execute(context)

        return {"message": "Презентация успешно удалена"}
    except PermissionError:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#########################################################################################
#
@presentation_router.get("/{entity_id}/publicate", response_model=PresentationResponse)
async def publicate_presentation(
    entity_id: int,
    request: Request,
):
    """
    Публикация презентации (генерация уникального кода публикации).
    """
    user_id = request.user.id  # Получаем ID владельца из запроса

    use_case = PresentationUseCasePublish()

    try:
        context = PresentationUseCasePublishContext(
            presentation_id=entity_id,
            user_id=user_id,
        )
        presentation = await use_case.execute(context)
        return PresentationResponse.model_validate(presentation)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
