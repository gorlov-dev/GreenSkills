from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Query

from app.use_cases.slide_template.read import SlideTemplateUseCaseRead
from app.use_cases.slide_template.read_list import (
    SlideTemplateUseCaseList,
    SlideTemplateUseCaseListContext,
)
from app.web_api.schemas.slide_template import SlideTemplateResponse

template_router = APIRouter(prefix="/template", tags=["Template"])


#########################################################################################
#
@template_router.get("/", response_model=List[SlideTemplateResponse])
async def list_slide_templates(
    sort_by: str = Query(default="updated_at", description="Поле для сортировки"),
    sort_order: str = Query(
        default="desc", description="Порядок сортировки (asc/desc)"
    ),
):
    """
    Получение списка шаблонов слайдов.
    """
    try:
        context = SlideTemplateUseCaseListContext(
            sort_by=sort_by, sort_order=sort_order
        )
        templates = await SlideTemplateUseCaseList().execute(context)
        return [SlideTemplateResponse.model_validate(t) for t in templates]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
