from datetime import datetime
from typing import Literal, Optional, List

from pydantic import BaseModel, ConfigDict, Field

from app.web_api.schemas.slide import SlideResponse


class PresentationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: Optional[str]
    publication_code: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    slides: List[SlideResponse]


class PresentationReorderSlideRequest(BaseModel):
    slide_id: int = Field(..., description="ID слайда")
    position: int = Field(..., ge=1, description="Новая позиция слайда")


class PresentationGenerateRequest(BaseModel):
    prompt: str = Field(..., description="Тема презентации")
    slides_count: int = Field(..., ge=1, description="Количество слайдов")


class PresentationListRequest(BaseModel):
    sort_by: str = Field(default="updated_at", description="Поле для сортировки")
    sort_order: Literal["asc", "desc"] = Field(
        default="desc", description="Порядок сортировки"
    )

class PresentationGenerateLLMRequest(BaseModel):
    """
    Схема для генерации структуры презентации через LLM
    """
    theme: str = Field(..., description="Тема презентации")
    relevant_chunks: List[str] = Field(
        default=[],
        description="Релевантные тексты или подсказки для улучшения генерации"
    )
