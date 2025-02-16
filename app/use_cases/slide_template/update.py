from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.entities.slide_template import SlideTemplateEntity
from app.adapters.db.session import async_session_maker


class SlideTemplateUseCaseUpdate:
    repository = SlideTemplateRepository()

    async def execute(self, payload: SlideTemplateEntity) -> SlideTemplateEntity:
        async with async_session_maker() as session:
            return await self.repository.update(session, payload)
