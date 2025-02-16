from celery import Celery
from app.config import Config

celery_app = Celery(
    "evstigney_tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_backend=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    broker_connection_retry_on_startup=True,
)

# Импортируем все задания, чтобы Celery знал о них
from app.tasks import generate_slide_prompts, notifications
