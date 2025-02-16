
from app.tasks import celery_app
from app.use_cases.rag.pdf_summarize import SummarizePdfUseCase, SummarizePdfContext
from app.services.pdf_chunk_service import PdfChunkService
from app.services.llm_service import LLMService
from loguru import logger

@celery_app.task
def summarize_pdf_task(pdf_path: str, chunk_size: int = 256) -> dict:
    """
    Celery-задача для асинхронного суммаризирования PDF.
    Возвращает словарь { "title": ..., "chunks": [...], "summaries": [...] }.
    """
    try:
        pdf_chunk_svc = PdfChunkService(
            encoding_name="cl100k_base",
            default_chunk_size=chunk_size,
        )
        llm_service = LLMService(
            model_url="http://127.0.0.1:8000/v1",
            model_name="t-tech/T-lite-it-1.0",
            open_api_key="EMPTY",
            temperature=0.4,
            stop_token_ids="",
        )

        use_case = SummarizePdfUseCase(pdf_chunk_svc, llm_service)

        context = SummarizePdfContext(pdf_path=pdf_path, chunk_size=chunk_size)
        result = use_case.execute_sync(context)

        return {
            "title": result.title,
            "chunks": result.chunks,
            "summaries": result.summaries,
        }
    except Exception as e:
        logger.error(f"Ошибка в summarize_pdf_task: {e}")
        return {"error": str(e)}
