from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import Book
from .schemas import BookCreateRequest, BookEditRequest


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_all_books_by_user(self, user_id: UUID, session: AsyncSession):
        statement = (
            select(Book).where(Book.user_id == user_id).order_by(desc(Book.created_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_id(self, book_id: UUID, session: AsyncSession):
        statement = select(Book).where(Book.id == book_id)
        result = await session.exec(statement)
        if not result:
            return None
        return result.first()

    async def create_book(
        self, book_data: BookCreateRequest, user_id: UUID, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.user_id = user_id
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(
        self, book_id: UUID, book_data: BookEditRequest, session: AsyncSession
    ):
        book = await self.get_book_by_id(book_id, session)
        if not book:
            return None

        book_data_dict = book_data.model_dump()

        for key, value in book_data_dict.items():
            setattr(book, key, value)
        await session.commit()
        return book

    async def delete_book_by_id(self, book_id: UUID, session: AsyncSession):
        book = await self.get_book_by_id(book_id, session)
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return {}
