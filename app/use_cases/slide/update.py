from typing import Any, Dict, Optional
from pydantic import BaseModel

from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.repositories.slide import SlideRepository
from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.entities.slide import SlideEntity
from app.adapters.db.session import async_session_maker


class SlideUseCaseUpdateContext(BaseModel):
    slide_id: int
    user_id: int
    template_id: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
    prompt: Optional[str] = None


class SlideUseCaseUpdate:
    repository = SlideRepository()
    presentation_repository = PresentationRepository()
    slide_template_repository = SlideTemplateRepository()

    async def execute(self, context: SlideUseCaseUpdateContext) -> SlideEntity:
        async with async_session_maker() as session:
            # 1. Получаем слайд
            slide = await self.repository.get_by_id(session, context.slide_id)
            if not slide:
                raise ValueError("Слайд не найден")

            presentation = await self.presentation_repository.get_by_id(
                session, slide.presentation_id
            )
            if not presentation:
                raise ValueError("Презентация не найдена")

            # 2. Проверяем, принадлежит ли слайд пользователю
            if presentation.owner_id != context.user_id:
                raise PermissionError("Вы не можете редактировать этот слайд")

            # 3. Обновляем данные слайда
            if context.template_id is not None:
                slide_template = await self.slide_template_repository.get_by_id(
                    session, context.template_id
                )
                if not slide_template:
                    raise ValueError("Шаблон слайда не найден")
                slide.template_id = context.template_id
            if context.data is not None:
                slide.data = context.data
            if context.prompt is not None:
                slide.prompt = context.prompt

            # 4. Сохраняем изменения
            return await self.repository.update(session, slide)
