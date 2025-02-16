from typing import Optional
from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseRead:
    repository = PresentationRepository()

    async def execute(self, payload: int) -> Optional[PresentationEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_by_id(session, payload)
