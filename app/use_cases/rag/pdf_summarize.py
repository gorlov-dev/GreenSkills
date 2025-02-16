import os
from typing import List
from pydantic import BaseModel
from app.services.pdf_chunk_service import PdfChunkService
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from loguru import logger


class SummarizePdfContext(BaseModel):
    pdf_path: str
    chunk_size: int = 256


class SummarizePdfResult(BaseModel):
    title: str
    chunks: List[str]
    summaries: List[str]
    embeddings: List[List[float]]  # Добавили эмбеддинги


class SummarizePdfUseCase:
    """
    Use-case для:
    1) Чтения PDF
    2) Деления на чанки
    3) Генерации кратких суммаризаций
    4) Генерации эмбеддингов для чанков
    """

    def __init__(
        self,
        pdf_chunk_service: PdfChunkService,
        llm_service: LLMService,
        embedding_service: EmbeddingService,  # добавили
    ):
        self.pdf_chunk_service = pdf_chunk_service
        self.llm_service = llm_service
        self.embedding_service = embedding_service  

    def execute_sync(self, context: SummarizePdfContext) -> SummarizePdfResult:
        """
        Синхронная версия метода, удобная для Celery.
        """
        logger.info(f"Начинаем суммаризацию для PDF: {context.pdf_path}")

        # 1️⃣ Читаем PDF
        text = self.pdf_chunk_service.read_pdf(context.pdf_path)
        logger.info(f"Текст из PDF прочитан (длина {len(text)} символов)")

        # 2️⃣ Делим на чанки
        chunks = self.pdf_chunk_service.split_text_into_chunks(
            text, chunk_size=context.chunk_size
        )
        logger.info(f"Разбили текст на {len(chunks)} чанков")

        # 3️⃣ Генерируем суммаризации для каждого чанка
        summaries = []
        for ch in chunks:
            summary = self.llm_service.summarize_text_chunk(ch)
            summaries.append(summary)
        logger.info(f"Получили суммаризации для всех чанков")

        # 4️⃣ Формируем эмбеддинги для чанков
        embeddings = self.embedding_service.encode_texts(chunks)
        logger.info(f"Сформировали {len(embeddings)} эмбеддингов")

        # 5️⃣ Формируем результат
        result = SummarizePdfResult(
            title=os.path.basename(context.pdf_path),
            chunks=chunks,
            summaries=summaries,
            embeddings=embeddings  # <-- Вставляем эмбеддинги в результат
        )
        logger.info(f"Готов результат суммаризации + эмбеддинги для: {result.title}")
        return result
