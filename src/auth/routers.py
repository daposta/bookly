from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.responses import JSONResponse
from .schemas import (
    User,
    UserLoginRequest,
    UserLoginResponse,
    UserSignupRequest,
    UserSignupResponse,
)
from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import UserService
from .utils import create_access_token, verify_password
from .middlewares import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from datetime import datetime

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    user_data: UserSignupRequest, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return JSONResponse(
        content={
            "message": "Registration successful",
            "user": {
                "id": str(new_user.id),
            },
        }
    )


@auth_router.post(
    "/login", response_model=UserLoginResponse, status_code=status.HTTP_201_CREATED
)
async def login(
    login_data: UserLoginRequest, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(
        user_data={
            "email": user.email,
            "user_id": str(user.id),
            "role": user.role,
        }
    )
    refresh_token = create_access_token(
        user_data={
            "email": user.email,
            "role": user.role,
        },
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        refresh=True,
    )
    return JSONResponse(
        content={
            "message": "Login succesful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "role": user.role,
            },
        }
    )


@auth_router.get(
    "/refresh-token",
    status_code=status.HTTP_200_OK,
)
async def get_new_access_token(
    token_info: dict = Depends(RefreshTokenBearer()),
) -> dict:
    expiry_timestamp = token_info["exp"]
    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    new_token_info = create_access_token(user_data=token_info["user"])

    return JSONResponse(
        content={
            "access_token": new_token_info,
        }
    )


@auth_router.get(
    "/me",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def revoke_token(
    token_info: dict = Depends(AccessTokenBearer()),
):
    jti = token_info["jti"]
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logout successful"}, status_code=status.HTTP_200_OK
    )
