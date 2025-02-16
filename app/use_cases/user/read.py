from typing import Optional
from app.adapters.db.repositories.user import UserRepository
from app.adapters.db.session import async_session_maker
from app.entities.user import UserEntity


class UserUseCaseRead:
    repository = UserRepository()

    async def execute(self, payload: int) -> Optional[UserEntity]:
        async with async_session_maker() as session:
            return await self.repository.get_by_id(session, payload)
