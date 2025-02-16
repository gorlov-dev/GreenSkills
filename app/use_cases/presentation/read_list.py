from typing import List, Optional
from pydantic import BaseModel

from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseListContext(BaseModel):
    user_id: Optional[int] = None
    sort_by: str = "updated_at"  # Поле для сортировки
    sort_order: str = "desc"  # asc или desc


class PresentationUseCaseList:
    repository = PresentationRepository()

    async def execute(
        self, context: PresentationUseCaseListContext
    ) -> List[PresentationEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_list(
                session=session,
                user_id=context.user_id,
                sort_by=context.sort_by,
                sort_order=context.sort_order,
            )
