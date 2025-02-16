from http import HTTPStatus

from pydantic import BaseModel
from starlette.exceptions import HTTPException


class WebApiBaseException(HTTPException):
    status_code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    detail = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.detail = message


class BadRequestException(WebApiBaseException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    detail = HTTPStatus.BAD_REQUEST.description


class NotFoundException(WebApiBaseException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    detail = HTTPStatus.NOT_FOUND.description


class ForbiddenException(WebApiBaseException):
    status_code = HTTPStatus.FORBIDDEN
    error_code = "FORBIDDEN"
    detail = "Отсутствуют права доступа"


class UnauthorizedException(WebApiBaseException):
    status_code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    detail = "Пользователь не авторизован"


class UnprocessableEntity(WebApiBaseException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(WebApiBaseException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    detail = HTTPStatus.UNPROCESSABLE_ENTITY.description


class ExceptionResponseSchema(BaseModel):
    error: str
