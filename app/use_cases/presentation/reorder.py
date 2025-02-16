import pprint
import random
from pydantic import BaseModel, Field

from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.adapters.db.session import async_session_maker
from app.adapters.db.repositories.slide import SlideRepository
from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseSlidesReorderContext(BaseModel):
    slide_id: int
    position: int = Field(..., ge=1)
    owner_id: int  # Для проверки владельца


class PresentationUseCaseSlidesReorder:
    slide_repository = SlideRepository()
    presentation_repository = PresentationRepository()

    async def execute(
        self, context: PresentationUseCaseSlidesReorderContext
    ) -> PresentationEntity:
        async with async_session_maker() as session:
            # 1. Получаем слайд
            slide = await self.slide_repository.get_by_id(session, context.slide_id)
            if not slide:
                raise ValueError("Слайд не найден")

            # 2. Получаем презентацию
            presentation = await self.presentation_repository.get_by_id(
                session, slide.presentation_id
            )
            if not presentation:
                raise ValueError("Презентация не найдена")

            # 3. Проверяем, принадлежит ли презентация пользователю
            if presentation.owner_id != context.owner_id:
                raise PermissionError("Вы не можете изменять эту презентацию")

            # 4. Получаем все слайды презентации, отсортированные по позиции
            slides = await self.slide_repository.get_by_presentation_id(
                session, presentation.id
            )
            slides.sort(key=lambda s: s.position)

            if context.position > len(slides):
                context.position = len(slides)

            # 5. Находим индекс текущего слайда
            slide_index = next(
                (i for i, s in enumerate(slides) if s.id == context.slide_id), None
            )
            if slide_index is None:
                raise ValueError("Слайд не найден в списке презентации")

            # 6. Удаляем слайд из текущей позиции и вставляем в новую
            slide_to_move = slides.pop(slide_index)
            slides.insert(context.position - 1, slide_to_move)

            # 8. Обновляем позиции слайдов
            for index, slide_ in enumerate(slides, start=1):
                slide_.position = index
                await self.slide_repository.update(session, slide_)

            await session.refresh(presentation)
            return presentation
