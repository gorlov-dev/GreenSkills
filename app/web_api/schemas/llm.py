from pydantic import BaseModel, Field
from typing import List

class LLMGenerateStructureRequest(BaseModel):
    """
    Схема для входных данных эндпоинта генерации структуры презентации
    """
    theme: str = Field(..., description="Тема презентации")
    relevant_chunks: List[str] = Field(
        default=[],
        description="Список релевантных текстов/подсказок для генерации"
    )