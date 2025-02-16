from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.entities.slide_template import SlideTemplateEntity
from app.adapters.db.session import async_session_maker


class SlideTemplateUseCaseDelete:
    repository = SlideTemplateRepository()

    async def execute(self, payload: int | SlideTemplateEntity) -> None:
        async with async_session_maker() as session:
            if isinstance(payload, int):
                entity = self.repository.get_by_id(session, payload)
            else:
                entity = payload

            if entity is None:
                raise ValueError("Шаблон не найден")

            await self.repository.delete(session, entity)
