from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class SlideTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str = Field(max_length=20)
    data: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None