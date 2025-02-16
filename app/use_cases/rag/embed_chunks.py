from typing import List
from pydantic import BaseModel
from app.services.embedding_service import EmbeddingService

class EmbedChunksContext(BaseModel):
    chunks: List[str]

class EmbedChunksResult(BaseModel):
    embeddings: List[List[float]]

class EmbedChunksUseCase:
    """
    Use-case для преобразования списка чанков в эмбеддинги через EmbeddingService.
    """

    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service

    def execute_sync(self, context: EmbedChunksContext) -> EmbedChunksResult:
        """
        Синхронная версия (удобна для вызова через Celery).
        """
        # Вызываем encode_texts
        vectors = self.embedding_service.encode_texts(context.chunks)
        return EmbedChunksResult(embeddings=vectors)
