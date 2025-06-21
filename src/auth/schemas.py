from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.books.schemas import Book
from src.reviews.schemas import Review


class UserSignupRequest(BaseModel):
    first_name: str = Field(
        min_length=2,
    )
    last_name: str = Field(
        min_length=2,
    )
    username: str = Field(min_length=5, max_length=10)
    password: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8 or not any(char.isdigit() for char in value):
            raise ValueError(
                "Password must be at least 8 chars long and must include at least one digit"
            )
        return value


class UserSignupResponse(BaseModel):
    message: str
    user: dict


class User(BaseModel):
    first_name: str
    last_name: str
    username: str = Field(min_length=6, max_length=10)
    email: str
    created_at: datetime
    update_at: datetime
    books: Optional[List[Book]]
    reviews: Optional[List[Review]]


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    user: dict
    access_token: str
    refresh_token: str
    message: str


class EmailModel(BaseModel):
    addresses: List[EmailStr]