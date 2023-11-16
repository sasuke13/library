from abc import ABC, abstractmethod
from typing import Iterable

from books.models import Book
from visitors.dto import VisitorRegistrationDTO, VisitorDTO, ReadingStatisticDTO, SessionDTO
from visitors.models import Visitor, Session


class VisitorRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def does_visitor_exist_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        pass

    @abstractmethod
    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        pass

    @abstractmethod
    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        pass


class VisitorInteractorInterface(VisitorRepositoryAndServiceInterface, ABC):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass


class SessionRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        pass

    @abstractmethod
    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        pass

    @abstractmethod
    def close_session(self, session: Session) -> str:
        pass


class SessionInteractorInterface(SessionRepositoryAndServiceInterface, ABC):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass

    @abstractmethod
    def close_session(self, visitor: Visitor) -> str:
        pass
