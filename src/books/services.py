from books.dto import CreateBookDTO
from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book
from reading_sessions.models import Session


class BookService(BookRepositoryAndServiceInterface):
    def __init__(self, book_repository: BookRepositoryAndServiceInterface):
        self.book_repository = book_repository

    def create_book(self, book_dto: CreateBookDTO) -> Book:
        return self.book_repository.create_book(book_dto)

    def get_book_by_id(self, book_id: int) -> Book:
        return self.book_repository.get_book_by_id(book_id)

    def get_all_books(self) -> Book:
        return self.book_repository.get_all_books()

    def add_total_reading_time_by_session(self, session: Session):
        return self.book_repository.add_total_reading_time_by_session(session)
