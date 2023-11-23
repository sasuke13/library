from abc import abstractmethod, ABC

from books.models import Book
from reading_sessions.dto import SessionDTO
from reading_sessions.models import Session
from visitors.models import Visitor


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
