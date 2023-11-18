from dataclasses import dataclass
from datetime import datetime
from itertools import repeat
from typing import Iterable

from django.db.models.sql import Query
from django.utils import timezone
from annoying.functions import get_object_or_None

from books.models import Book
from core.abstract_classes import AbstractRepository
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.exceptions import VisitorAlreadyExists, SessionDoesNotExist
from visitors.interfaces import VisitorRepositoryAndServiceInterface, SessionRepositoryAndServiceInterface, \
    DTOConverterInterface, ReadingStatisticRepositoryAndServiceInterface
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

    def add_total_reading_time_by_session(self, session: Session):
        visitor = session.visitor
        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        if visitor.total_reading_time:
            visitor.total_reading_time = visitor.total_reading_time + total_reading_time

        else:
            visitor.total_reading_time = total_reading_time

        visitor.save()


class SessionRepository(SessionRepositoryAndServiceInterface, AbstractRepository):

    def get_all_sessions_dto_by_visitor(self, visitor: Visitor) -> Iterable[SessionDTO]:
        active_session = visitor.sessions.all()

        return map(self.converter.to_dto, active_session, repeat(SessionDTO))

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        active_session = visitor.sessions.filter(is_active=True).all().first()

        if not active_session:
            raise SessionDoesNotExist()

        return active_session

    def get_active_session_by_book(self, book: Book) -> Session:
        active_session = book.sessions.filter(is_active=True).all().first()

        return active_session

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        session = Session.objects.create(visitor=visitor, book=book)

        return self.converter.to_dto(session, SessionDTO)

    def close_session(self, session: Session) -> str:
        book = session.book

        session.is_active = False
        session.session_end = timezone.now()

        session.save()

        book.last_used = datetime.now()

        book.save()

        return 'Session has been successfully closed!'


class DTOConverterRepository(DTOConverterInterface, AbstractRepository):

    def convert_to_dto(self, dto_class: dataclass, query: Query) -> dataclass:
        return self.converter.to_dto(query, dto_class)

    def convert_many_to_dto(self, dto_class: dataclass, query: Iterable[Query]) -> Iterable[dataclass]:
        return map(self.converter.to_dto, query, repeat(dto_class))


class ReadingStatisticRepository(ReadingStatisticRepositoryAndServiceInterface):

    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        statistic = ReadingStatistic.objects.create(
            book=session.book,
            visitor=session.visitor,
            total_reading_time=total_reading_time
        )

        return statistic

    def add_total_reading_time_to_existing_statistic(
            self,
            session: Session,
            statistic: ReadingStatistic
    ) -> ReadingStatistic:

        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        statistic.total_reading_time += total_reading_time

        statistic.save()

        return statistic

    def get_all_statistics(self) -> ReadingStatistic:
        return ReadingStatistic.objects.all()

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        return visitor.statistics.all()

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        statistic = visitor.statistics.filter(book=book).first()

        return statistic

    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        statistic = session.visitor.statistics.filter(book=session.book).first()

        return statistic
