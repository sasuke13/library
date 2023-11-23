from typing import Iterable

from books.dto import BookListViewDTO, BookDTO
from books.interfaces import BookRepositoryAndServiceInterface, BookInteractorInterface
from core.interfaces import DTOConverterInterface


class BookInteractor(BookInteractorInterface):
    def __init__(
            self,
            book_service: BookRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface
    ):
        self.book_service = book_service
        self.converter_service = converter_service

    def get_book_dto_by_id(self, book_id: int) -> BookDTO:
        book = self.book_service.get_book_by_id(book_id)

        book_dto = self.converter_service.convert_to_dto(BookDTO, book)

        return book_dto

    def get_all_books_dto(self) -> Iterable[BookListViewDTO]:
        books = self.book_service.get_all_books()

        books_dto = self.converter_service.convert_many_to_dto(BookListViewDTO, books)
        print(books)
        print(books_dto)
        return books_dto
