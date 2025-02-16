from app.tasks import celery_app
from app.web_api.utils.event_dispatcher import event_dispatcher


@celery_app.task
async def send_notification_task(user_id: int, message: str):
    """Фоновая задача для отправки уведомления через WebSocket"""
    await event_dispatcher.send_all(user_id, "notification", {"message": message})
