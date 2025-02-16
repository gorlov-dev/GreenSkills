from typing import Any, Dict, Optional
from pydantic import BaseModel

from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.repositories.slide import SlideRepository
from app.entities.slide import SlideEntity
from app.adapters.db.session import async_session_maker


class SlideUseCaseCreateContext(BaseModel):
    user_id: int
    template_id: int
    presentation_id: int
    prompt: Optional[str] = None
    position: int
    data: Optional[Dict[str, Any]] = None


class SlideUseCaseCreate:
    repository = SlideRepository()
    presentation_repository = PresentationRepository()

    async def execute(self, context: SlideUseCaseCreateContext) -> SlideEntity:
        async with async_session_maker() as session:
            presentation = await self.presentation_repository.get_by_id(
                session, context.presentation_id
            )
            if not presentation:
                raise ValueError("Презентация не найдена")

            if presentation.owner_id != context.user_id:
                raise PermissionError("Недостаточно прав")

            entity = SlideEntity(
                prompt=context.prompt,
                template_id=context.template_id,
                presentation_id=context.presentation_id,
                position=context.position,
                data=context.data,
            )
            slide = await self.repository.create(session, entity)

            slides = await self.repository.get_by_presentation_id(
                session, presentation.id
            )
            slides.sort(key=lambda s: s.position)

            slide_index = next(
                (i for i, s in enumerate(slides) if s.id == slide.id), None
            )
            if slide_index is None:
                raise ValueError("Слайд не найден в списке презентации")

            slide_to_move = slides.pop(slide_index)
            slides.insert(context.position - 1, slide_to_move)

            for index, slide_ in enumerate(slides, start=1):
                slide_.position = index
                await self.repository.update(session, slide_)

            await session.refresh(slide)
            return slide
