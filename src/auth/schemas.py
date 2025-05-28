from datetime import datetime
from pydantic import BaseModel, Field, field_validator, EmailStr


class UserSignupRequest(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=5, max_length=10)
    password: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8 or not any(char.is_digit() for char in value):
            raise ValueError(
                "Password must be at least 8 chars long and must include at least one digit"
            )
        return value


class UserSignupResponse(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=6, max_length=10)
    email: str
    created_at: datetime
    update_at: datetime


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    user: dict
    access_token: str
    refresh_token: str
    message: str
