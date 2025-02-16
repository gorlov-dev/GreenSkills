from typing import Generic, TypeVar, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.adapters.db.session import async_session_maker
from sqlalchemy import delete

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, entity_class: Type[T]):
        self.entity = entity_class

    async def get_by_id(self, session: AsyncSession, payload: int) -> Optional[T]:
        stmt = select(self.entity).where(self.entity.id == payload)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, payload: T) -> T:
        session.add(payload)
        await session.commit()
        await session.refresh(payload)
        return payload

    async def update(self, session: AsyncSession, payload: T) -> T:
        await session.commit()
        await session.refresh(payload)
        return payload

    async def delete(self, session: AsyncSession, payload: T) -> None:
        stmt = delete(self.entity).where(self.entity.id == payload.id)
        await session.execute(stmt)
        await session.commit()
