from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from src.reviews.schemas import Review


class BookCreateRequest(BaseModel):
    title: str
    author: str
    description: str


class Book(BookCreateRequest):
    id: UUID
    created_at: datetime
    update_at: datetime


class BookDetailResponse(Book):
    reviews: List[Review]


class BookCreateResponse(Book):
    ...
    # class Config:
    #     orm_mode = True


class BookEditRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None


class BookEditResponse(Book): ...
