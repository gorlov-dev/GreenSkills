import random
import string
from pydantic import BaseModel
from app.adapters.db.repositories.presentation import PresentationRepository
from app.entities.presentation import PresentationEntity
from app.adapters.db.session import async_session_maker


async def generate_unique_code(repository: PresentationRepository, session) -> str:
    """Генерирует уникальный код публикации."""
    while True:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        is_unique = await repository.is_publication_code_unique(session, code)
        if is_unique:
            return code


class PresentationUseCasePublishContext(BaseModel):
    presentation_id: int
    user_id: int  # Для проверки владельца


class PresentationUseCasePublish:
    repository = PresentationRepository()

    async def execute(
        self, context: PresentationUseCasePublishContext
    ) -> PresentationEntity:
        async with async_session_maker() as session:
            # 1. Получаем презентацию по ID
            presentation = await self.repository.get_by_id(
                session, context.presentation_id
            )
            if not presentation:
                raise ValueError("Презентация не найдена")

            if presentation.publication_code:
                raise ValueError("Презентация уже опубликована")

            # 2. Проверяем, принадлежит ли презентация пользователю
            if presentation.owner_id != context.user_id:
                raise PermissionError("Вы не можете публиковать эту презентацию")

            # 3. Генерируем уникальный код публикации
            presentation.publication_code = await generate_unique_code(
                self.repository, session
            )

            # 4. Сохраняем изменения
            await self.repository.update(session, presentation)

            return presentation
