from app.adapters.db.repositories.user import UserRepository
from app.entities.user import UserEntity
from app.adapters.db.session import async_session_maker


class UserUseCaseDelete:
    repository = UserRepository()

    async def execute(self, payload: int | UserEntity) -> None:
        async with async_session_maker() as session:
            if isinstance(payload, int):
                user_entity = self.repository.get_by_id(session, payload)
            else:
                user_entity = payload

            if user_entity is None:
                raise ValueError("Пользователь не найден")

            await self.repository.delete(session, user_entity)
