
from src.books.schemas import  BookCreateRequest

books_prefix = "/api/v1/books"
def test_get_all_books(fake_session, fake_book_service, test_client):
    response = test_client.get(url=f"{books_prefix}")

    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_once_with(fake_session)


def test_add_book(fake_session, fake_book_service, test_client):
    book_data_dict = {
        "title": "dayton",
         "author": "secret",
        "description": "secret",


    }


    book_data= BookCreateRequest(**book_data_dict)
    response = test_client.post(url=f"{books_prefix}", json=book_data.model_dump())

    assert fake_book_service.create_book_called_once()
    assert fake_book_service.create_book_called_once_with(book_data, fake_session)
