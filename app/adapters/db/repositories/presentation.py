from typing import List, Optional

from sqlalchemy import asc, desc, select
from app.adapters.db.base_repository import BaseRepository
from app.entities.presentation import PresentationEntity
from sqlalchemy.ext.asyncio import AsyncSession


class PresentationRepository(BaseRepository[PresentationEntity]):
    def __init__(self):
        super().__init__(PresentationEntity)

    async def get_list(
        self,
        session: AsyncSession,
        user_id: Optional[int] = None,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
    ) -> List[PresentationEntity]:
        """Получить список презентаций с фильтрацией и сортировкой."""
        stmt = select(PresentationEntity)

        # Фильтр по пользователю (если указан)
        if user_id is not None:
            stmt = stmt.where(PresentationEntity.owner_id == user_id)

        # Определяем порядок сортировки
        sort_field = getattr(PresentationEntity, sort_by, PresentationEntity.updated_at)
        order_by = desc(sort_field) if sort_order == "desc" else asc(sort_field)
        stmt = stmt.order_by(order_by)

        result = await session.execute(stmt)
        return result.scalars().all()

    async def is_publication_code_unique(
        self, session: AsyncSession, payload: str
    ) -> bool:
        """Проверяет, существует ли уже такой код публикации."""
        stmt = select(PresentationEntity).where(
            PresentationEntity.publication_code == payload
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is None

    async def get_by_publication_code(
        self, session: AsyncSession, publication_code: str
    ) -> Optional[PresentationEntity]:
        """Получить презентацию по коду публикации."""
        stmt = select(PresentationEntity).where(
            PresentationEntity.publication_code == publication_code
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
