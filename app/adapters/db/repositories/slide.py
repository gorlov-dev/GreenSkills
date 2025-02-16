from typing import List

from sqlalchemy import select
from app.adapters.db.base_repository import BaseRepository
from app.entities.slide import SlideEntity
from sqlalchemy.ext.asyncio import AsyncSession


class SlideRepository(BaseRepository[SlideEntity]):
    def __init__(self):
        super().__init__(SlideEntity)

    async def get_by_presentation_id(
        self, session: AsyncSession, presentation_id: int
    ) -> List[SlideEntity]:
        """Получить все слайды, принадлежащие указанной презентации, отсортированные по позиции."""
        stmt = (
            select(SlideEntity)
            .where(SlideEntity.presentation_id == presentation_id)
            .order_by(SlideEntity.position)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
