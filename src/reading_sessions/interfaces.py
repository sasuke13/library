from abc import abstractmethod, ABC

from books.models import Book
from reading_sessions.dto import SessionDTO
from reading_sessions.models import Session
from visitors.models import Visitor


class SessionRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def get_all_sessions(self) -> Session:
        """
        Makes query of all sessions.
        :return Session instance:
        """
        pass

    @abstractmethod
    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        """
        Gets an active session of visitor.
        Raises SessionDoesNotExist if user haven't active session.
        :param visitor:
        :return Session instance:
        """
        pass

    @abstractmethod
    def get_active_session_by_book(self, book: Book) -> Session:
        """
        Gets an active session of book.
        :param book:
        :return Session instance:
        """
        pass

    @abstractmethod
    def get_all_sessions_by_visitor(self, visitor: Visitor) -> Session:
        """
        Gets all visitor's sessions
        :param visitor:
        :return Session instance:
        """
        pass

    @abstractmethod
    def open_session(self, visitor: Visitor, book: Book) -> Session:
        """
        Creates session passing on visitor and book instances.
        :param visitor:
        :param book:
        :return Session instance:
        """
        pass

    @abstractmethod
    def close_session(self, session: Session) -> str:
        """
        Gets book by session.
        Makes session inactive and sets end of session.
        Sets last_used field for book.
        :param session:
        :return message for response:
        """
        pass


class SessionInteractorInterface(ABC):
    @abstractmethod
    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        """
        Accepts book id and gets the book instance or
        raises BookDoesNotExist error if book does not exist.
        Tries to get session by the gotten book and
        if it returns a Session instance, raises BookIsAlreadyTaken error.
        Tries to get an active session by visitor and if it returns the session it becomes
        closed, and adds total reading time for the current book.
        Opens a brand-new session.
        Converts create Session instance into SessionDTO instance
        :param visitor:
        :param book_id:
        :return SessionDTO instance:
        """
        pass

    @abstractmethod
    def close_session(self, visitor: Visitor) -> str:
        """
        Gets visitor's active session.
        Gets statistic by active session.
        Closes the session.
        Adds session duration to total reading time to book.
        If statistic was not found it creates a new one.
        Adds total reading time to statistic.
        :param visitor:
        :return message for response:
        """
        pass

    @abstractmethod
    def get_active_session_dto_by_visitor(self, visitor: Visitor) -> SessionDTO:
        """
        Gets visitor's active session.
        Converts Session instance into SessionDTO.
        :param visitor:
        :return SessionDTO instance:
        """
        pass
