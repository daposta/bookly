from sqlmodel import SQLModel, Field, Column, String, Relationship
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional
from sqlalchemy import ForeignKey
from src.auth import models


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    )
    title: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    author: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    description: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default_factory=datetime.now)
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default_factory=datetime.now)
    )

    user: Optional["models.User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    )
    book_id: Optional[uuid.UUID] = Field(
        sa_column=Column(pg.UUID(as_uuid=True), ForeignKey("books.id"), nullable=True)
    )
    review_text: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    rating: int = Field(lt=5)

    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    user: Optional["models.User"] = Relationship(back_populates="reviews")
    book: Optional["models.Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review book: {self.book_id} by user: {self.user_id}>"
