from dataclasses import dataclass
from datetime import datetime
from itertools import repeat
from typing import Iterable

from auto_dataclass.dj_model_to_dataclass import ToDTOConverter
from django.db.models.sql import Query
from django.utils import timezone
from annoying.functions import get_object_or_None

from books.models import Book
from visitors.dto import VisitorRegistrationDTO
from visitors.exceptions import VisitorAlreadyExists, SessionDoesNotExist
from visitors.interfaces import VisitorRepositoryAndServiceInterface, SessionRepositoryAndServiceInterface, \
    DTOConverterInterface, ReadingStatisticRepositoryAndServiceInterface
from visitors.models import Visitor, ReadingStatistic, Session


class VisitorRepository(VisitorRepositoryAndServiceInterface):
    def does_visitor_exist_by_email(self, email: str) -> bool:
        visitor = get_object_or_None(Visitor.objects.
                                     prefetch_related('statistics', 'sessions'), email=email)

        if visitor:
            raise VisitorAlreadyExists(f'Visitor with email {email} already exists!')

        return False

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        registered_visitor = Visitor.objects.create_user(**visitor_registration_dto.__dict__)

        return registered_visitor

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


class SessionRepository(SessionRepositoryAndServiceInterface):
    def get_all_sessions(self) -> Session:
        sessions = (Session.objects.all().order_by('visitor', 'book').
                    prefetch_related('visitor', 'book').select_related('visitor', 'book'))

        return sessions

    def get_all_sessions_by_visitor(self, visitor: Visitor) -> Session:
        sessions = visitor.sessions.prefetch_related('visitor', 'book').select_related('visitor', 'book')

        return sessions

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        active_session = (visitor.sessions.filter(is_active=True).all().first().
                          prefetch_related('visitor', 'book').select_related('visitor', 'book'))

        if not active_session:
            raise SessionDoesNotExist()

        return active_session

    def get_active_session_by_book(self, book: Book) -> Session:
        active_session = (book.sessions.filter(is_active=True).all().first().
                          prefetch_related('visitor', 'book').select_related('visitor', 'book'))

        return active_session

    def open_session(self, visitor: Visitor, book: Book) -> Session:
        session = Session.objects.create(visitor=visitor, book=book)

        return session

    def close_session(self, session: Session) -> str:
        book = session.book

        session.is_active = False
        session.session_end = timezone.now()

        session.save()

        book.last_used = datetime.now()

        book.save()

        return 'Session has been successfully closed!'


class DTOConverterRepository(DTOConverterInterface):
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter

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
        return (ReadingStatistic.objects.all().order_by('visitor', 'book').
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        return (visitor.statistics.all().
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_all_statistics_by_book(self, book: Book) -> ReadingStatistic:
        return (book.statistics.all().
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        statistic = (visitor.statistics.filter(book=book).first().
                     prefetch_related('book', 'visitor').
                     select_related('book', 'visitor'))

        return statistic

    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        statistic = (session.visitor.statistics.filter(book=session.book).first().
                     prefetch_related('book', 'visitor').
                     select_related('book', 'visitor'))

        return statistic
