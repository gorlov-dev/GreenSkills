from app.adapters.db.repositories.user import UserRepository
from app.entities.user import UserEntity
from app.adapters.db.session import async_session_maker


class UserUseCaseUpdate:
    repository = UserRepository()

    async def execute(self, payload: UserEntity) -> UserEntity:
        async with async_session_maker() as session:
            return await self.repository.update(session, payload)
