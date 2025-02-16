from pydantic import BaseModel
from app.adapters.db.repositories.presentation import PresentationRepository
from app.adapters.db.session import async_session_maker
from app.use_cases.presentation.reorder import SlideRepository


class PresentationUseCaseDeleteContext(BaseModel):
    presentation_id: int
    user_id: int


class PresentationUseCaseDelete:
    repository = PresentationRepository()
    slide_repository = SlideRepository()

    async def execute(self, context: PresentationUseCaseDeleteContext) -> None:
        async with async_session_maker() as session:
            presentation = await self.repository.get_by_id(
                session, context.presentation_id
            )

            if presentation is None:
                raise ValueError("Презентация не найдена")

            if presentation.owner_id != context.user_id:
                raise PermissionError("Недостаточно прав")

            slides = await self.slide_repository.get_by_presentation_id(
                session, presentation.id
            )

            for slide in slides:
                await self.slide_repository.delete(session, slide)

            await self.repository.delete(session, presentation)
