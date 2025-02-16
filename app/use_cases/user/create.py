from pydantic import BaseModel, Field, EmailStr

from app.adapters.db.repositories.user import UserRepository
from app.entities.user import UserEntity
from app.utils.hash_password import hash_password
from app.adapters.db.session import async_session_maker


class UserUseCaseCreateContext(BaseModel):
    email: EmailStr
    login: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    password: str = Field(max_length=255)


class UserUseCaseCreate:
    repository = UserRepository()

    async def execute(self, user_data: UserUseCaseCreateContext) -> UserEntity:
        async with async_session_maker() as session:
            if await self.repository.email_exist(session, str(user_data.email)):
                raise ValueError(
                    f"Пользователь с почтой {user_data.email} уже существует"
                )
            if await self.repository.login_exist(session, user_data.login):
                raise ValueError(
                    f"Пользователь с логином {user_data.login} уже существует"
                )

            hashed_password = hash_password(user_data.password)
            user = UserEntity(
                email=str(user_data.email),
                login=user_data.login,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                password=hashed_password,
                is_active=True,
            )
            return await self.repository.create(session, user)
