from abc import ABC, abstractmethod
from typing import Iterable

from books.dto import BookDTO, BookListViewDTO
from books.models import Book


class BookRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        pass

    @abstractmethod
    def get_all_books(self) -> Book:
        pass


class BookInteractorInterface(ABC):
    @abstractmethod
    def get_book_dto_by_id(self, book_id: int) -> BookDTO:
        pass

    @abstractmethod
    def get_all_books_dto(self) -> Iterable[BookListViewDTO]:
        pass
