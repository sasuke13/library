from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import repeat
from typing import Iterable

from auto_dataclass.dj_model_to_dataclass import ToDTOConverter
from django.db.models.sql import Query
from annoying.functions import get_object_or_None

from reading_sessions.models import Session
from visitors.dto import VisitorRegistrationDTO
from visitors.exceptions import VisitorAlreadyExists
from visitors.interfaces import VisitorRepositoryAndServiceInterface, DTOConverterInterface
from visitors.models import Visitor


class VisitorRepository(VisitorRepositoryAndServiceInterface):
    def does_visitor_exist_by_email(self, email: str) -> bool:
        visitor = get_object_or_None(Visitor.objects.
                                     prefetch_related('statistics', 'sessions'), email=email)

        if visitor:
            raise VisitorAlreadyExists(f'Visitor with email {email} already exists!')

        return False

    def get_all_visitors(self) -> Visitor:
        today_date = datetime.now()

        visitors = (
            Visitor.objects.all().
            prefetch_related('sessions', 'statistics').
            filter(
                sessions__session_end__range=[today_date - timedelta(days=7), today_date],
                sessions__is_active=False
            )
        )

        return visitors

    def change_total_reading_time_for_the_last_week(self, visitor: Visitor):
        today_date = datetime.now()

        sessions = (
            visitor.sessions.all().
            filter(
                session_end__range=[today_date - timedelta(days=7), today_date], is_active=False
            )
        )

        visitor.total_reading_time_for_the_last_week = timedelta(0)
        for session in sessions:
            session_start = session.session_start
            session_end = session.session_end
            total_reading_time = session_end - session_start

            visitor.total_reading_time_for_the_last_week = (
                visitor.total_reading_time_for_the_last_week + total_reading_time
            )

        visitor.save()

    def change_total_reading_time_for_the_last_month(self, visitor: Visitor):
        today_date = datetime.now()

        sessions = (
            visitor.sessions.all().
            filter(
                session_end__range=[today_date - timedelta(days=30), today_date], is_active=False
            )
        )
        visitor.total_reading_time_for_the_last_week = timedelta(0)
        for session in sessions:
            session_start = session.session_start
            session_end = session.session_end
            total_reading_time = session_end - session_start

            visitor.total_reading_time_for_the_last_month = (
                visitor.total_reading_time_for_the_last_month + total_reading_time
            )

        visitor.save()

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        registered_visitor = Visitor.objects.create_user(**visitor_registration_dto.__dict__)

        return registered_visitor

    def add_total_reading_time_by_session(self, session: Session):
        book = session.book

        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        book.total_reading_time = book.total_reading_time + total_reading_time

        book.save()


class DTOConverterRepository(DTOConverterInterface):
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter

    def convert_to_dto(self, dto_class: dataclass, query: Query) -> dataclass:
        return self.converter.to_dto(query, dto_class)

    def convert_many_to_dto(self, dto_class: dataclass, query: Iterable[Query]) -> Iterable[dataclass]:
        return map(self.converter.to_dto, query, repeat(dto_class))
