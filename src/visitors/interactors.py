from typing import Iterable

from books.interfaces import BookRepositoryAndServiceInterface
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.exceptions import SessionDoesNotExist
from visitors.interfaces import VisitorRepositoryAndServiceInterface, VisitorInteractorInterface, \
    SessionRepositoryAndServiceInterface, SessionInteractorInterface
from visitors.models import Visitor, Session


class VisitorInteractor(VisitorInteractorInterface):
    def __init__(
            self,
            visitor_service: VisitorRepositoryAndServiceInterface,
            book_service: BookRepositoryAndServiceInterface
    ):
        self.visitor_service = visitor_service
        self.book_service = book_service

    def does_visitor_exist_by_email(self, email: str) -> bool:
        return self.visitor_service.does_visitor_exist_by_email(email)

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        self.does_visitor_exist_by_email(visitor_registration_dto.email)

        return self.visitor_service.registration(visitor_registration_dto)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        return self.visitor_service.get_users_statistic_dto(visitor)

    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        book = self.book_service.get_book_by_id(book_id)

        return self.visitor_service.open_session(visitor, book)


class SessionInteractor(SessionInteractorInterface):
    def __init__(
            self,
            session_service: SessionRepositoryAndServiceInterface,
            book_service: BookRepositoryAndServiceInterface
    ):
        self.session_service = session_service
        self.book_service = book_service

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_service.get_active_session_by_visitor(visitor)

    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        book = self.book_service.get_book_by_id(book_id)

        try:
            active_session = self.session_service.get_active_session_by_visitor(visitor)
            self.session_service.close_session(active_session)

        except SessionDoesNotExist:
            return self.session_service.open_session(visitor, book)

    def close_session(self, visitor: Visitor) -> str:
        active_session = self.session_service.get_active_session_by_visitor(visitor)

        return self.session_service.close_session(active_session)
