from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.responses import JSONResponse

from src import mail
from src.config import Config
from src.errors import InvalidToken, UserAlreadyExists, UserNotFound
from src.mail import create_message
from .schemas import (
    EmailModel,
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
from .utils import (
    create_access_token,
    decode_url_safe_token,
    generate_url_safe_token,
    verify_password,
)
from .dependencies import (
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


@auth_router.post("/send-mail")
async def send_mails(emails: EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to Bookly</h1>"
    message = create_message(recipients=emails, subject="Welcome", body=html)
    await mail.send_message(message)
    return JSONResponse(content={"message": "Email sent successfully"})


@auth_router.get("/verify")
async def verify_email(emails: EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to Bookly</h1>"
    message = create_message(recipients=emails, subject="Welcome", body=html)
    await mail.send_message(message)
    return JSONResponse(content={"message": "Email sent successfully"})


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    data = decode_url_safe_token(token)
    user_email = data.get("email")
    if user_email is None:
        return JSONResponse(
            content={"message": "Error occurred during verification"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    user = await user_service.get_user_by_email(user_email, session)
    if user is None:
        raise UserNotFound()
    await user_service.update_user(user, {"is_verified": True}, session)
    html = "<h1>Bookly Account Activated</h1>"
    message = create_message(
        recipients=[user_email], subject="Account activated", body=html
    )
    await mail.send_message(message)
    return JSONResponse(
        content={"message": "Account verified successfuly"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.post(
    "/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    user_data: UserSignupRequest, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)
    token = generate_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify{token}"
    html = f"""
    <h1>Welcome to Bookly</h1>
    <p>Please click this <a href="{link}">Link</a> to verify your email. </p>
    """
    message = create_message(
        recipients=[email], subject="Verify your account", body=html
    )
    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Account created. Check your email to verify account",
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
        raise UserNotFound()

    if not verify_password(login_data.password, user.password):
        raise UserNotFound()

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
        raise InvalidToken()

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
