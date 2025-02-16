from typing import Optional, List
import random
from pydantic import BaseModel

from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.repositories.slide import SlideRepository
from app.adapters.db.repositories.slide_template import SlideTemplateRepository
from app.entities.presentation import PresentationEntity
from app.entities.slide import SlideEntity
from app.adapters.db.session import async_session_maker


class PresentationUseCaseGenerateFakeContext(BaseModel):
    owner_id: int
    prompt: Optional[str] = None
    slides_count: int


class PresentationUseCaseGenerateFake:
    presentation_repository = PresentationRepository()
    slide_repository = SlideRepository()
    slide_template_repository = SlideTemplateRepository()

    async def execute(
        self, context: PresentationUseCaseGenerateFakeContext
    ) -> PresentationEntity:
        async with async_session_maker() as session:
            # 1. Создаем новую презентацию
            presentation = PresentationEntity(
                owner_id=context.owner_id, prompt=context.prompt
            )
            presentation = await self.presentation_repository.create(
                session, presentation
            )

            slide_templates = await self.slide_template_repository.get_list(session)
            if not slide_templates:
                raise ValueError("Нет доступных шаблонов слайдов")

            # 3. Генерируем случайные темы слайдов
            slide_titles = self._generate_fake_slide_titles(context.slides_count)

            slides = []
            for index, title in enumerate(slide_titles, start=1):
                # Случайный выбор шаблона
                selected_template = random.choice(slide_templates)

                slide = SlideEntity(
                    presentation_id=presentation.id,
                    template_id=selected_template.id,
                    position=index,
                    prompt=title,
                    data=selected_template.data,
                )

                slides.append(await self.slide_repository.create(session, slide))

            await session.refresh(presentation)
            return presentation

    def _generate_fake_slide_titles(self, count: int) -> List[str]:
        """Генерирует случайные темы слайдов."""
        topics = [
            "Основные тренды индустрии",
            "История развития темы",
            "Современные вызовы",
            "Ключевые технологии",
            "Будущие перспективы",
            "Практические кейсы",
            "Ошибки и решения",
            "Заключение и выводы",
        ]

        return random.sample(topics, min(count, len(topics)))
