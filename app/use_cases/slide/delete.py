from pydantic import BaseModel
from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.repositories.slide import SlideRepository
from app.adapters.db.session import async_session_maker


class SlideUseCaseDeleteContext(BaseModel):
    slide_id: int
    user_id: int


class SlideUseCaseDelete:
    repository = SlideRepository()
    presentation_repository = PresentationRepository()

    async def execute(self, context: SlideUseCaseDeleteContext) -> None:
        async with async_session_maker() as session:
            slide = await self.repository.get_by_id(session, context.slide_id)

            if slide is None:
                raise ValueError("Слайд не найден")

            presentation = await self.presentation_repository.get_by_id(
                session, slide.presentation_id
            )
            if not presentation:
                raise ValueError("Презентация не найдена")

            if presentation.owner_id != context.user_id:
                raise PermissionError("Недостаточно прав")

            await self.repository.delete(session, slide)
