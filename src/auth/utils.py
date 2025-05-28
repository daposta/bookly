from datetime import timedelta, datetime
import jwt
from passlib.context import CryptContext
from src.config import Config
import uuid
import logging
from typing import Union, Any

password_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(user_password: str) -> str:
    return password_context.hash(user_password)


def verify_password(user_password: str, hashed_password: str) -> bool:
    return password_context.verify(user_password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    print(user_data)
    payload: dict[str, Any] = {}
    payload["user"] = user_data
    expire_at = datetime.now() + (expiry or timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["exp"] = int(expire_at.timestamp())

    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict | None:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=Config.SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )

        return decoded

    except jwt.ExpiredSignatureError:
        logging.exception("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logging.exception("Invalid token:", str(e))
        return None
