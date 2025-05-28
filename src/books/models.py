from sqlmodel import SQLModel, Field, Column, String
from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import Optional


class Book(SQLModel, table=True):
    __tablename__ = "books"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    user_id: Optional[uuid.UUID] = Field(
        sa_column=Column(foreign_key="users.id", default=None)
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
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    def __repr__(self):
        return f"<Book {self.title}>"
