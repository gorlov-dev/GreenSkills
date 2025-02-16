from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseUpdate:
    repository = PresentationRepository()

    async def execute(self, payload: PresentationEntity) -> PresentationEntity:
        async with async_session_maker() as session:
            return await self.repository.update(session, payload)
