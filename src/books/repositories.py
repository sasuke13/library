from annoying.functions import get_object_or_None

from books.exceptions import BookDoesNotExist
from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book
from core.abstract_classes import AbstractRepository


class BookRepository(BookRepositoryAndServiceInterface, AbstractRepository):
    def get_book_by_id(self, book_id: int) -> Book:
        book = get_object_or_None(Book, pk=book_id)

        if not book:
            raise BookDoesNotExist(f'Book with id {book_id} does not exist!')

        return book
