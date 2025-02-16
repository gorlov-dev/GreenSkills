from celery import Task
from app.adapters.db.session import async_session_maker


class BaseTask(Task):
    """Базовый класс для всех Celery-задач"""

    async def run_with_db(self, func, *args, **kwargs):
        """Запуск задачи с сессией базы данных"""
        async with async_session_maker() as session:
            return await func(session, *args, **kwargs)
