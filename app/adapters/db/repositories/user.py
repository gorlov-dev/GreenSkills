from typing import Optional

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.db.base_repository import BaseRepository
from app.entities.user import UserEntity


class UserRepository(BaseRepository[UserEntity]):
    def __init__(self):
        super().__init__(UserEntity)

    async def email_exist(self, session: AsyncSession, payload: str) -> bool:
        stmt = select(UserEntity).where(UserEntity.email == payload)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def login_exist(self, session: AsyncSession, payload: str) -> bool:
        stmt = select(UserEntity).where(UserEntity.login == payload)
        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_by_email_or_login(
        self, session: AsyncSession, payload: str
    ) -> Optional[UserEntity]:
        stmt = select(UserEntity).where(
            (UserEntity.login == payload) | (UserEntity.email == payload)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
