from typing import Iterable

from books.interfaces import BookRepositoryAndServiceInterface
from core.interfaces import DTOConverterInterface
from reading_statistics.dto import ReadingStatisticDTO, ReadingStatisticWithBookTotalReadingTimeDTO
from reading_statistics.interfaces import (
    ReadingStatisticInteractorInterface,
    ReadingStatisticRepositoryAndServiceInterface
)
from visitors.models import Visitor


class ReadingStatisticInteractor(ReadingStatisticInteractorInterface):
    def __init__(
            self,
            reading_statistic_service: ReadingStatisticRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface,
            book_service: BookRepositoryAndServiceInterface
    ):
        self.reading_statistic_service = reading_statistic_service
        self.converter_service = converter_service
        self.book_service = book_service

    def get_all_statistics_dto(self) -> Iterable[ReadingStatisticWithBookTotalReadingTimeDTO]:
        statistics = self.reading_statistic_service.get_all_statistics()
        statistics_dto = self.converter_service.convert_many_to_dto(
            ReadingStatisticWithBookTotalReadingTimeDTO,
            statistics
        )

        return statistics_dto

    def get_all_statistics_dto_by_visitor(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        statistics = self.reading_statistic_service.get_all_statistics_by_visitor(visitor)
        statistics_dto = self.converter_service.convert_many_to_dto(ReadingStatisticDTO, statistics)

        return statistics_dto

    def get_all_statistics_dto_by_book(self, book_id: int) -> Iterable[ReadingStatisticWithBookTotalReadingTimeDTO]:
        book = self.book_service.get_book_by_id(book_id)
        statistic = self.reading_statistic_service.get_all_statistics_by_book(book)
        statistic_dto = self.converter_service.convert_many_to_dto(
            ReadingStatisticWithBookTotalReadingTimeDTO,
            statistic
        )

        return statistic_dto

    def get_statistic_dto_by_visitor_and_book(self, visitor: Visitor, book_id: int) -> ReadingStatisticDTO:
        book = self.book_service.get_book_by_id(book_id)
        statistic = self.reading_statistic_service.get_statistic_by_visitor_and_book(visitor, book)

        statistic_dto = self.converter_service.convert_to_dto(ReadingStatisticDTO, statistic)

        return statistic_dto
