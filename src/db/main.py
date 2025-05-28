from sqlmodel import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import Config
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

DB_URL = Config.DB_URL  # "postgresql+asyncpg://postgres:s3cr3t@localhost:5435/expodb"


import ssl

ssl_context = ssl.create_default_context()

async_engine: AsyncEngine = create_async_engine(
    url=DB_URL, connect_args={"ssl": False}, echo=True
)


async def init_db():
    try:
        async with async_engine.begin() as conn:
            from src.books.models import Book
            from src.auth.models import User

            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Failed to connect: {e}")


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with Session() as session:
        yield session
