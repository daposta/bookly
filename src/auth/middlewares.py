from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends

from src.errors import InvalidRole, InvalidToken, RefreshTokenRequired
from .models import User
from src.db.main import get_session
from src.db.redis import check_token_in_blocklist
from .utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import UserService
from typing import List

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_content = decode_token(token)

        if not self.validate_token(token):
            raise InvalidToken()
        if await check_token_in_blocklist(token_content["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or revoked.",
                    "resolution": "Please get a new token",
                },
            )

        self.verify_token_data(token_content)
        return token_content

    def validate_token(self, token) -> bool:
        token_data = decode_token(token)
        return True if token_data is not None else False

    def verify_token_data(self, token_content: dict):
        raise NotImplementedError("Please provide an implementation in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_content: dict):
        if token_content and token_content["refresh"]:
            raise InvalidToken()
        # HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Please provide an access token",
        #     )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_content: dict):
        if token_content and not token_content["refresh"]:
            raise RefreshTokenRequired()
        # HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Please provide a refresh token",
        #     )


async def get_current_user(
    user_info: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = user_info["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise InvalidRole()
        # HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="You are not permitted to do this operation",
        #     )
