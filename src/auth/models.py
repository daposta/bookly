from datetime import datetime
import uuid
from sqlmodel import Column, Field, SQLModel, String, Boolean
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    username: str = Field(sa_column=Column(String, nullable=False, unique=True))
    first_name: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    last_name: str = Field(
        sa_column=Column(
            String,
            nullable=False,
        )
    )
    email: str = Field(sa_column=Column(String, nullable=False, unique=True))
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, unique=True, server_default="user")
    )
    password: str = Field(
        exclude=True,
        sa_column=Column(
            String,
            nullable=False,
        ),
    )
    is_verified: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now)
    )

    def __repr__(self):
        return f"<User {self.email}>"
