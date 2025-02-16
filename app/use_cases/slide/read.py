from typing import Optional
from app.adapters.db.repositories.slide import SlideRepository
from app.entities.slide import SlideEntity
from app.adapters.db.session import async_session_maker


class SlideUseCaseRead:
    repository = SlideRepository()

    async def execute(self, payload: int) -> Optional[SlideEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_by_id(session, payload)
