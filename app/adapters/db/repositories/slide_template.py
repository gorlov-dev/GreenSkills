from typing import List
from sqlalchemy import asc, desc, select
from app.adapters.db.base_repository import BaseRepository
from app.entities.slide_template import SlideTemplateEntity
from sqlalchemy.ext.asyncio import AsyncSession


class SlideTemplateRepository(BaseRepository[SlideTemplateEntity]):
    def __init__(self):
        super().__init__(SlideTemplateEntity)

    async def get_list(
        self,
        session: AsyncSession,
        sort_by: str = "updated_at",
        sort_order: str = "desc",
    ) -> List[SlideTemplateEntity]:
        """Получить список шаблонов слайдов с сортировкой."""
        stmt = select(SlideTemplateEntity)

        # Определяем порядок сортировки
        sort_field = getattr(
            SlideTemplateEntity, sort_by, SlideTemplateEntity.updated_at
        )
        order_by = desc(sort_field) if sort_order == "desc" else asc(sort_field)
        stmt = stmt.order_by(order_by)

        result = await session.execute(stmt)
        return result.scalars().all()
