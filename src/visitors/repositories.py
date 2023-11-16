from datetime import datetime
from itertools import repeat
from typing import Iterable

from annoying.functions import get_object_or_None

from books.models import Book
from core.abstract_classes import AbstractRepository
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.exceptions import VisitorAlreadyExists, SessionDoesNotExist
from visitors.interfaces import VisitorRepositoryAndServiceInterface, SessionRepositoryAndServiceInterface
from visitors.models import Visitor, ReadingStatistic, Session


class VisitorRepositoryAndService(VisitorRepositoryAndServiceInterface, AbstractRepository):
    def does_visitor_exist_by_email(self, email: str) -> bool:
        visitor = get_object_or_None(Visitor, email=email)

        if visitor:
            raise VisitorAlreadyExists(f'Visitor with email {email} already exists!')

        return False

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        registered_visitor = Visitor.objects.create_user(**visitor_registration_dto.__dict__)

        return self.converter.to_dto(registered_visitor, VisitorDTO)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        statistics = ReadingStatistic.objects.select_related(
            'visitor',
            'book'
        ).filter(visitor=visitor)

        return map(self.converter.to_dto, statistics, repeat(ReadingStatisticDTO))

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        active_session = visitor.sessions.filter(is_active=True).all().first()

        if active_session:
            active_session.is_active = False
            active_session.session_end = datetime.now()

        session = Session.objects.create(visitor=visitor, book=book)

        return self.converter.to_dto(session, SessionDTO)


class SessionRepository(SessionRepositoryAndServiceInterface, AbstractRepository):

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        active_session = visitor.sessions.filter(is_active=True).all().first()

        if not active_session:
            raise SessionDoesNotExist()

        return active_session

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        session = Session.objects.create(visitor=visitor, book=book)

        return self.converter.to_dto(session, SessionDTO)

    def close_session(self, session: Session) -> str:
        session.is_active = False
        session.session_end = datetime.now()

        session.save()

        return 'Session has been successfully closed!'
