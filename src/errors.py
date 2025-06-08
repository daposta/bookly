from typing import Any, Callable
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BaseException(Exception):
    """Base class for all exceptions"""

    pass


class InvalidToken(BaseException):
    """User used invalid tokens"""

    # pass


class RevokedToken(BaseException):
    """User used invalid tokens"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class AccessTokenRequired(BaseException):
    """User provided refresh token where access token is required"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class RefreshTokenRequired(BaseException):
    """User provided an access token where a refresh token is required"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class UserAlreadyExists(BaseException):
    """User provided an email for a user that already exists"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class InsufficientPermission(BaseException):
    """User does not have necessary permission to perform an action"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class BookNotFound(BaseException):
    """Book with id not found"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


class UserNotFound(BaseException):
    """User not found"""

    pass

    # def __init__(self, message: str, detail: dict):
    #     super().__init__(*args)


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BaseException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler
