from typing import List
from fastapi import APIRouter, HTTPException

from app.use_cases.presentation.read_by_code import (
    PresentationUseCaseReadByCode,
    PresentationUseCaseReadByCodeContext,
)
from app.web_api.schemas.presentation import (
    PresentationResponse,
)

presentation_router = APIRouter(prefix="/presentation", tags=["Presentation"])


#########################################################################################
#
@presentation_router.get(
    "/published/{publication_code}", response_model=PresentationResponse
)
async def get_presentation_by_code(publication_code: str):
    """
    Получение презентации по коду публикации.
    """
    use_case = PresentationUseCaseReadByCode()

    context = PresentationUseCaseReadByCodeContext(publication_code=publication_code)
    presentation = await use_case.execute(context)

    if presentation is None:
        raise HTTPException(status_code=404, detail="Презентация не найдена")

    return PresentationResponse.model_validate(presentation)
