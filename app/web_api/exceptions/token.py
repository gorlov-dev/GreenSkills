from app.web_api.exceptions.base import WebApiBaseException


class DecodeTokenException(WebApiBaseException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(WebApiBaseException):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"
