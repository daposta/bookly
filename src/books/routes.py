from uuid import UUID
from fastapi import APIRouter, Depends
from typing import List

from fastapi import status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import (
    BookCreateRequest,
    BookCreateResponse,
    BookDetailResponse,
    BookEditRequest,
    Book,
)


from src.books.services import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_routes = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["user"]))


async def get_book_by_id(book_id: UUID, session):
    book = await book_service.get_book_by_id(book_id, session)
    return book


@book_routes.post(
    "/",
    response_model=BookCreateResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_checker],
)
async def add_book(
    book_data: BookCreateRequest,
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    user_id = token_info.get("user")["user_id"]
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@book_routes.get(
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


@book_routes.get(
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


@book_routes.get(
    "/{book_id}",
    response_model=BookDetailResponse,
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


@book_routes.patch(
    "/{book_id}",
    response_model=BookCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def edit_book(
    book_id: UUID,
    book_data: BookEditRequest,
    session: AsyncSession = Depends(get_session),
    token_info=Depends(access_token_bearer),
):
    book = await book_service.update_book(book_id, book_data, session)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No book with matching id"
        )
    return book


@book_routes.delete(
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
