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
        """
        Makes query of all statistics.
        :return all ReadingStatistic instances:
        """
        pass

    @abstractmethod
    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        """
        Makes query of visitor's statistics.
        :param visitor:
        :return ReadingStatistic instance:
        """
        pass

    @abstractmethod
    def get_all_statistics_by_book(self, book: Book) -> ReadingStatistic:
        """
        Makes query of book's statistics
        :param book:
        :return ReadingStatistic instance:
        """
        pass

    @abstractmethod
    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        """
        Makes query of user's statistics with certain book
        :param visitor:
        :param book:
        :return ReadingStatistic instance:
        """
        pass

    @abstractmethod
    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        """
        Gets statistic through related name in session.
        :param session:
        :return ReadingStatistic instance:
        """
        pass

    @abstractmethod
    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        """
        Creates ReadingStatistic instance using session instance and
        book instance gotten from session.
        :param session:
        :return ReadingStatistic instance:
        """
        pass

    @abstractmethod
    def add_total_reading_time_to_existing_statistic(
            self,
            session: Session,
            statistic: ReadingStatistic
    ) -> ReadingStatistic:
        """
        Subtracts duration of session with total_reading_time field
        in existing statistic
        :param session:
        :param statistic:
        :return ReadingStatistic instance:
        """
        pass


class ReadingStatisticInteractorInterface(ABC):
    @abstractmethod
    def get_all_statistics_dto(self) -> Iterable[ReadingStatisticDTO]:
        """
        Gets all statistics and converts them into ReadingStatisticDTO instances.
        :return Many ReadingStatisticDTO instances:
        """
        pass

    @abstractmethod
    def get_all_statistics_dto_by_visitor(self, visitor: Visitor) -> Iterable[ReadingStatistic]:
        """
        Gets all visitor's statistics and converts them into ReadingStatisticDTO instances.
        :param visitor:
        :return Many ReadingStatisticDTO instances:
        """
        pass

    @abstractmethod
    def get_all_statistics_dto_by_book(self, book_id: int) -> ReadingStatistic:
        """
        Gets all book's statistics and converts them into ReadingStatisticDTO instances.
        :param book_id:
        :return Many ReadingStatisticDTO instances:
        """
        pass

    @abstractmethod
    def get_statistic_dto_by_visitor_and_book(self, visitor: Visitor, book_id: Book) -> ReadingStatisticDTO:
        """
        Gets visitor's statistic with a certain book and
        converts it into ReadingStatisticDTO instances.
        :param visitor:
        :param book_id:
        :return Many ReadingStatisticDTO instances:
        """
        pass
