from pydantic import Field, BaseModel

from app.adapters.db.repositories.user import UserRepository
from app.entities.user import UserEntity
from app.utils.hash_password import verify_password
from app.adapters.db.session import async_session_maker


class AuthUseCaseLoginContext(BaseModel):
    identity: str = Field(max_length=255)
    password: str = Field(max_length=255)


class AuthUseCaseLogin:
    repository = UserRepository()

    async def execute(self, payload: AuthUseCaseLoginContext) -> UserEntity:
        async with async_session_maker() as session:
            user = await self.repository.get_by_email_or_login(
                session, payload.identity
            )

            if user is None:
                raise ValueError("Ошибка авторизации")

            if not verify_password(payload.password, user.password):
                raise ValueError("Ошибка авторизации")

            return user
