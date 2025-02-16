from typing import Optional
from pydantic import BaseModel
from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseReadByCodeContext(BaseModel):
    publication_code: str


class PresentationUseCaseReadByCode:
    repository = PresentationRepository()

    async def execute(
        self, context: PresentationUseCaseReadByCodeContext
    ) -> Optional[PresentationEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_by_publication_code(
                session, context.publication_code
            )
