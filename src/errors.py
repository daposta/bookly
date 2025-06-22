from typing import Any, Callable
from fastapi import FastAPI, status
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


class InvalidRole(BaseException):
    """User has the wrong role"""

    pass


class AccountNotVerified(BaseException):
    """Account not verified"""

    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BaseException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Token is valid or expired",
                "error_code": "invalid_token",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a refresh token",
                "error_code": "invalid_refresh_token",
            },
        ),
    )

    app.add_exception_handler(
        InvalidRole,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You are not permitted to do this operation",
                "error_code": "invalid_role",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not found",
                "error_code": "account_not_found",
                "resolution": "Please check your email for verification details",
            },
        ),
    )
