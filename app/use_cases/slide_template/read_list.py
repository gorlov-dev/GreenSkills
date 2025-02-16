from typing import List, Optional
from pydantic import BaseModel

from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.adapters.db.session import async_session_maker
from app.entities.slide_template import SlideTemplateEntity


class SlideTemplateUseCaseListContext(BaseModel):
    sort_by: str = "updated_at"
    sort_order: str = "desc"


class SlideTemplateUseCaseList:
    repository = SlideTemplateRepository()

    async def execute(
        self, context: SlideTemplateUseCaseListContext
    ) -> List[SlideTemplateEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_list(
                session=session, sort_by=context.sort_by, sort_order=context.sort_order
            )
