from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from books.models import Book
from reading_sessions.models import Session
from reading_statistics.models import ReadingStatistic
from visitors.dto import ReadingStatisticDTO
from visitors.models import Visitor


class ReadingStatisticRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_all_statistics(self) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_all_statistics_by_book(self, book: Book) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        pass

    @abstractmethod
    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        pass

    @abstractmethod
    def add_total_reading_time_to_existing_statistic(
            self,
            session: Session,
            statistic: ReadingStatistic
    ) -> ReadingStatistic:
        pass


class ReadingStatisticInteractorInterface(ABC):
    @abstractmethod
    def get_all_statistics_dto(self) -> Iterable[ReadingStatisticDTO]:
        pass

    @abstractmethod
    def get_all_statistics_dto_by_visitor(self, visitor: Visitor) -> Iterable[ReadingStatistic]:
        pass

    @abstractmethod
    def get_all_statistics_dto_by_book(self, book_id: int) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_statistic_dto_by_visitor_and_book(self, visitor: Visitor, book_id: Book) -> ReadingStatisticDTO:
        pass


class DTOConverterInterface(ABC):
    @abstractmethod
    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        pass

    @abstractmethod
    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        pass
