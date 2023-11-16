from abc import ABC, abstractmethod

from books.models import Book


class BookRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        pass
