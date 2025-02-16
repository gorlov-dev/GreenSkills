# app/web_api/routes/protected/rag.py

from fastapi import APIRouter, HTTPException, Request
from app.web_api.schemas.rag import SummarizePdfRequest, SummarizePdfResponse
from app.use_cases.rag.pdf_summarize import (
    SummarizePdfUseCase,
    SummarizePdfContext,
)
from app.services.pdf_chunk_service import PdfChunkService
from app.services.llm_service import LLMService
from loguru import logger

rag_router = APIRouter(prefix="/rag", tags=["RAG"])

@rag_router.post("/summarize-pdf", response_model=SummarizePdfResponse)
async def summarize_pdf(
    request: Request,
    payload: SummarizePdfRequest
):
    """
    Принимает путь к PDF и возвращает JSON со списком чанков и суммаризаций.
    """
    try:
        # Инициализируем сервисы
        pdf_chunk_svc = PdfChunkService(
            encoding_name="cl100k_base",
            default_chunk_size=payload.chunk_size,
        )
        llm_service = LLMService(
            model_url="http://127.0.0.1:8000/v1",
            model_name="t-tech/T-lite-it-1.0",
            open_api_key="EMPTY",
            temperature=0.4,
            stop_token_ids=""
        )

        # Формируем контекст
        context = SummarizePdfContext(
            pdf_path=payload.pdf_path,
            chunk_size=payload.chunk_size
        )

        # UseCase
        use_case = SummarizePdfUseCase(pdf_chunk_svc, llm_service)
        result = await use_case.execute(context)

        # Возвращаем результат
        return SummarizePdfResponse(
            title=result.title,
            chunks=result.chunks,
            summaries=result.summaries
        )
    except Exception as e:
        logger.error(f"Ошибка при RAG суммаризации: {e}")
        raise HTTPException(status_code=400, detail=str(e))
