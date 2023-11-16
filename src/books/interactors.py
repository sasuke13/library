from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book


class BookInteractor:
    def __init__(self, book_service: BookRepositoryAndServiceInterface):
        self.book_service = book_service

    def get_book_by_id(self, book_id: int) -> Book:
        return self.book_service.get_book_by_id(book_id)
