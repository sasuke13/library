from abc import ABC, abstractmethod
from typing import Iterable

from books.dto import BookDTO, BookListViewDTO
from books.models import Book
from reading_sessions.models import Session


class BookRepositoryAndServiceInterface(ABC):
    # @abstractmethod
    # def create_book(self, a):
    #     ...
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Book:
        """
        Makes query by id to get book instance or
        raises BookDoesNotExist if book was not found.
        :param book_id:
        :return Book instance:
        """
        pass

    @abstractmethod
    def get_all_books(self) -> Book:
        """
        Makes query to get all books.
        :return Book instance:
        """
        pass

    @abstractmethod
    def add_total_reading_time_by_session(self, session: Session):
        """
        Adds the duration of session in Book's total_reading_time field
        :param session:
        :return:
        """
        pass


class BookInteractorInterface(ABC):
    @abstractmethod
    def get_book_dto_by_id(self, book_id: int) -> BookDTO:
        """
        Gets Book instance by id
        and converts it into BookDTO instance
        :param book_id:
        :return BookDTO instance:
        """
        pass

    @abstractmethod
    def get_all_books_dto(self) -> Iterable[BookListViewDTO]:
        """
        Gest all books and converts them into BookListViewDTO instances.
        :return many BookListViewDTO instances:
        """
        pass
