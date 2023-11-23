from books.models import Book
from reading_sessions.interfaces import SessionRepositoryAndServiceInterface
from reading_sessions.models import Session
from visitors.models import Visitor


class SessionService(SessionRepositoryAndServiceInterface):
    def __init__(self, session_repository: SessionRepositoryAndServiceInterface):
        self.session_repository = session_repository

    def get_all_sessions(self) -> Session:
        return self.session_repository.get_all_sessions()

    def get_all_sessions_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_repository.get_all_sessions_by_visitor(visitor)

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_repository.get_active_session_by_visitor(visitor)

    def get_active_session_by_book(self, book: Book) -> Session:
        return self.session_repository.get_active_session_by_book(book)

    def open_session(self, visitor: Visitor, book: Book) -> Session:
        return self.session_repository.open_session(visitor, book)

    def close_session(self, session: Session) -> str:
        return self.session_repository.close_session(session)
