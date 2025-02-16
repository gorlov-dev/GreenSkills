# app/web_api/schemas/rag.py
from pydantic import BaseModel, Field
from typing import List

class SummarizePdfRequest(BaseModel):
    pdf_path: str = Field(..., description="Путь к PDF-файлу на сервере")
    chunk_size: int = Field(256, description="Размер чанка в токенах")

class SummarizePdfResponse(BaseModel):
    title: str
    chunks: List[str]
    summaries: List[str]
    embeddings: List[List[float]]   