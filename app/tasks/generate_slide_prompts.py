import time
from app.tasks import celery_app
from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.repositories.slide import SlideRepository
from app.web_api.utils.event_dispatcher import event_dispatcher
from app.tasks.base_task import BaseTask


@celery_app.task(base=BaseTask)
async def generate_presentation_task(
    session, owner_id: int, session_id: str, presentation_id: int, slides_count: int
):
    """Фоновая генерация презентации"""

    repository = PresentationRepository()
    slide_repository = SlideRepository()

    presentation = await repository.get_by_id(session, presentation_id)
    if not presentation:
        return

    # for i in range(1, slides_count + 1):
    #     slide = await slide_repository.create(
    #         session,
    #         {
    #             "presentation_id": presentation_id,
    #             "position": i,
    #             "data": {"title": f"Слайд {i}", "content": "Описание..."},
    #         },
    #     )

    #     # Отправляем промежуточные данные через WebSocket
    #     await event_dispatcher.send(
    #         owner_id, session_id, "slide_generated", {"slide": slide}
    #     )

    #     time.sleep(1)  # Имитация обработки

    # Завершение генерации
    await event_dispatcher.send(
        owner_id,
        session_id,
        "generation_completed",
        {"presentation_id": presentation_id},
    )
