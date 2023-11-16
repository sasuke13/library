from typing import Iterable

from books.models import Book
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.interfaces import VisitorRepositoryAndServiceInterface, SessionRepositoryAndServiceInterface
from visitors.models import Visitor, Session


class VisitorServiceAndService(VisitorRepositoryAndServiceInterface):
    def __init__(self, visitor_repository: VisitorRepositoryAndServiceInterface):
        self.visitor_repository = visitor_repository

    def does_visitor_exist_by_email(self, email: str) -> bool:
        return self.visitor_repository.does_visitor_exist_by_email(email)

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        return self.visitor_repository.registration(visitor_registration_dto)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        return self.visitor_repository.get_users_statistic_dto(visitor)

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        return self.visitor_repository.open_session(visitor, book)


class SessionService(SessionRepositoryAndServiceInterface):
    def __init__(self, session_repository: SessionRepositoryAndServiceInterface):
        self.session_repository = session_repository

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_repository.get_active_session_by_visitor(visitor)

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        return self.session_repository.open_session(visitor, book)

    def close_session(self, session: Session) -> str:
        return self.session_repository.close_session(session)
