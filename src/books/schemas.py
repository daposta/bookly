from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Book(BaseModel):
    id: UUID
    title: str
    author: str
    description: str
    created_at: datetime
    update_at: datetime


class BookCreateRequest(BaseModel):
    title: str
    author: str
    description: str


class BookCreateResponse(Book):
    ...
    # class Config:
    #     orm_mode = True


class BookEditRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None


class BookEditResponse(Book): ...
