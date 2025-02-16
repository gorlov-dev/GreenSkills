from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.web_api.schemas.slide_template import SlideTemplateResponse


class SlideResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data: Optional[Dict[str, Any]]
    position: int
    prompt: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    template: Optional[SlideTemplateResponse]


class SlideCreateRequest(BaseModel):
    template_id: int = Field(..., description="ID шаблона слайда")
    presentation_id: int = Field(
        ..., description="ID презентации, в которую добавляется слайд"
    )
    prompt: Optional[str] = Field(None, description="Промпт для генерации слайда")
    position: int = Field(..., ge=1, description="Позиция слайда в презентации")
    data: Optional[Dict[str, Any]] = Field(
        None, description="Дополнительные данные слайда"
    )


class SlideUpdateRequest(BaseModel):
    template_id: Optional[int] = Field(None, ge=1, description="ID шаблона")
    data: Optional[Dict[str, Any]] = Field(
        None, description="Обновленные данные слайда"
    )
    prompt: Optional[str] = Field(None, description="Промпт для слайда")
