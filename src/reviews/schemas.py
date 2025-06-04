from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ReviewCreateRequest(BaseModel):
    review_text: str
    rating: int = Field(lt=5)


class Review(ReviewCreateRequest):
    id: UUID
    # title: str
    user_id: UUID
    book_id: UUID
    # description: str
    created_at: datetime
    update_at: datetime
