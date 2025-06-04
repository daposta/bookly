from uuid import UUID
from fastapi import APIRouter, Depends
from typing import List

from fastapi import status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import (
    BookCreateRequest,
    BookCreateResponse,
    BookEditRequest,
    Book,
)


from src.books.services import BookService
from src.db.main import get_session
from src.auth.middlewares import AccessTokenBearer, RoleChecker
from src.reviews.services import ReviewService
from .schemas import Review, ReviewCreateRequest

reviews_router = APIRouter()
book_service = BookService()
review_service = ReviewService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["user"]))


async def get_book_by_id(book_id: UUID, session):
    book = await book_service.get_book_by_id(book_id, session)
    return book


@reviews_router.post(
    "/book/{book_id}",
    response_model=Review,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def add_book(
    book_id: UUID,
    book_data: ReviewCreateRequest,
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    user_id = token_info.get("user")["user_id"]
    book = book_service.get_book_by_id(book_id, session)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Book with id not found"},
        )
    new_book = await review_service.add_review_to_book(
        user_id, book_id, book_data, session
    )
    return new_book


@reviews_router.get(
    "/",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    return await book_service.get_all_books(session)


@reviews_router.get(
    "/users/{user_id}",
    response_model=List[Book],
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_user_books(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    return await book_service.get_all_books_by_user(user_id, session)


@reviews_router.get(
    "/{book_id}",
    response_model=Book,
    status_code=status.HTTP_200_OK,
    dependencies=[role_checker],
)
async def get_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    book = await get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book with matching id"
        )
    return book


@reviews_router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker],
)
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    user=Depends(access_token_bearer),
):
    book = await book_service.delete_book_by_id(book_id, session)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book with matching id"
        )
    return {}
