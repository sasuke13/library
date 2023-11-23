from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from books.models import Book
from visitors.dto import VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.models import Visitor, Session


class VisitorRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def change_total_reading_time_for_the_last_week(self, visitor: Visitor):
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self, visitor: Visitor):
        pass

    @abstractmethod
    def get_all_visitors(self) -> Visitor:
        pass

    @abstractmethod
    def does_visitor_exist_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        pass

    @abstractmethod
    def add_total_reading_time_by_session(self, session: Session):
        pass


class VisitorInteractorInterface(ABC):
    @abstractmethod
    def change_total_reading_time_for_the_last_week(self):
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self):
        pass

    @abstractmethod
    def get_all_visitors(self) -> Visitor:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        pass


class SessionRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_all_sessions(self) -> Session:
        pass

    @abstractmethod
    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        pass

    @abstractmethod
    def get_active_session_by_book(self, book: Book) -> Session:
        pass

    @abstractmethod
    def get_all_sessions_by_visitor(self, visitor: Visitor) -> Session:
        pass

    @abstractmethod
    def open_session(self, visitor: Visitor, book: Book) -> Session:
        pass

    @abstractmethod
    def close_session(self, session: Session) -> str:
        pass


class SessionInteractorInterface(ABC):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass

    @abstractmethod
    def close_session(self, visitor: Visitor) -> str:
        pass

    @abstractmethod
    def get_active_session_dto_by_visitor(self, visitor: Visitor) -> SessionDTO:
        pass


class DTOConverterInterface(ABC):
    @abstractmethod
    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        pass

    @abstractmethod
    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        pass
