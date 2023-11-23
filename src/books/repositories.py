from annoying.functions import get_object_or_None

from books.dto import CreateBookDTO
from books.exceptions import BookDoesNotExist
from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book
from reading_sessions.models import Session


class BookRepository(BookRepositoryAndServiceInterface):
    def create_book(self, book_dto: CreateBookDTO) -> Book:
        book = Book.objects.create(**book_dto.__dict__)

        return book

    def get_book_by_id(self, book_id: int) -> Book:
        book = get_object_or_None(Book, pk=book_id)

        if not book:
            raise BookDoesNotExist(f'Book with id {book_id} does not exist!')

        return book

    def get_all_books(self) -> Book:
        books = Book.objects.all().prefetch_related('sessions', 'statistics')

        return books

    def add_total_reading_time_by_session(self, session: Session):
        book = session.book

        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        book.total_reading_time = book.total_reading_time + total_reading_time

        book.save()
