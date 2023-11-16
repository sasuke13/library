from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book


class BookService(BookRepositoryAndServiceInterface):
    def __init__(self, book_repository: BookRepositoryAndServiceInterface):
        self.book_repository = book_repository

    def get_book_by_id(self, book_id: int) -> Book:
        return self.book_repository.get_book_by_id(book_id)
