from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from books.models import Book
from visitors.dto import VisitorRegistrationDTO, VisitorDTO, ReadingStatisticDTO, SessionDTO
from visitors.models import Visitor, Session, ReadingStatistic


class VisitorRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def does_visitor_exist_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        pass

    @abstractmethod
    def add_total_reading_time_by_session(self, session: Session):
        pass


class VisitorInteractorInterface(VisitorRepositoryAndServiceInterface):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass


class SessionRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        pass

    @abstractmethod
    def get_active_session_by_book(self, book: Book) -> Session:
        pass

    @abstractmethod
    def get_all_sessions_dto_by_visitor(self, visitor: Visitor) -> Iterable[SessionDTO]:
        pass

    @abstractmethod
    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        pass

    @abstractmethod
    def close_session(self, session: Session) -> str:
        pass


class SessionInteractorInterface(SessionRepositoryAndServiceInterface):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass

    @abstractmethod
    def close_session(self, visitor: Visitor) -> str:
        pass

    @abstractmethod
    def get_active_session_dto_by_visitor(self, visitor: Visitor) -> SessionDTO:
        pass


class ReadingStatisticRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_all_statistics(self) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
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
    def get_statistic_dto_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatisticDTO:
        pass

    @abstractmethod
    def get_all_statistics(self) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        pass

    @abstractmethod
    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        pass


class DTOConverterInterface(ABC):
    @abstractmethod
    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        pass

    @abstractmethod
    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        pass
