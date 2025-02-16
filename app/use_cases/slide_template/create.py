from typing import Any, Dict
from pydantic import BaseModel, Field

from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.entities.slide_template import SlideTemplateEntity
from app.adapters.db.session import async_session_maker


class SlideTemplateUseCaseCreateContext(BaseModel):
    title: str
    slug: str = Field(max_length=20)
    data: Dict[str, Any]


class SlideTemplateUseCaseCreate:
    repository = SlideTemplateRepository()

    async def execute(
        self, context: SlideTemplateUseCaseCreateContext
    ) -> SlideTemplateEntity:
        async with async_session_maker() as session:
            entity = SlideTemplateEntity(
                title=context.title,
                slug=context.slug,
                data=context.data,
            )
            return await self.repository.create(session, entity)
