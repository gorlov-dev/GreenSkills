from starlette.authentication import (
    AuthenticationBackend,
    AuthCredentials,
    AuthenticationError,
)
from starlette.requests import HTTPConnection
from app.entities.user import UserEntity
from app.use_cases.user.read import UserUseCaseRead
from app.web_api.utils.token_helper import TokenHelper


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        """
        Проверяет заголовок Authorization и возвращает пользователя.
        """
        auth_header = conn.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return AuthCredentials(["unauthenticated"]), None

        token = auth_header.split("Bearer ")[-1]

        try:
            payload = TokenHelper.decode(token)
            if "user_id" not in payload:
                raise AuthenticationError("Некорректный токен")
        except Exception:
            raise AuthenticationError("Неверный или истёкший токен")

        user: UserEntity = await UserUseCaseRead().execute(payload["user_id"])

        if not user or not user.is_active:
            return AuthCredentials(["unauthenticated"]), None

        return AuthCredentials(["authenticated"]), user
