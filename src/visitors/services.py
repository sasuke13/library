from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from books.models import Book
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.interfaces import VisitorRepositoryAndServiceInterface, SessionRepositoryAndServiceInterface, \
    DTOConverterInterface, ReadingStatisticRepositoryAndServiceInterface
from visitors.models import Visitor, Session, ReadingStatistic


class VisitorServiceAndService(VisitorRepositoryAndServiceInterface):
    def __init__(self, visitor_repository: VisitorRepositoryAndServiceInterface):
        self.visitor_repository = visitor_repository

    def does_visitor_exist_by_email(self, email: str) -> bool:
        return self.visitor_repository.does_visitor_exist_by_email(email)

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        return self.visitor_repository.registration(visitor_registration_dto)

    def add_total_reading_time_by_session(self, session: Session):
        self.visitor_repository.add_total_reading_time_by_session(session)


class SessionService(SessionRepositoryAndServiceInterface):
    def __init__(self, session_repository: SessionRepositoryAndServiceInterface):
        self.session_repository = session_repository

    def get_all_sessions_dto_by_visitor(self, visitor: Visitor) -> Iterable[SessionDTO]:
        return self.session_repository.get_all_sessions_dto_by_visitor(visitor)

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_repository.get_active_session_by_visitor(visitor)

    def get_active_session_by_book(self, book: Book) -> Session:
        return self.session_repository.get_active_session_by_book(book)

    def open_session(self, visitor: Visitor, book: Book) -> SessionDTO:
        return self.session_repository.open_session(visitor, book)

    def close_session(self, session: Session) -> str:
        return self.session_repository.close_session(session)


class DTOConverterService(DTOConverterInterface):
    def __init__(self, converter_repository: DTOConverterInterface):
        self.converter_repository = converter_repository

    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        return self.converter_repository.convert_to_dto(dto_class, query)

    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        return self.converter_repository.convert_many_to_dto(dto_class, query)


class ReadingStatisticService(ReadingStatisticRepositoryAndServiceInterface):
    def __init__(self, reading_statistic_repository: ReadingStatisticRepositoryAndServiceInterface):
        self.reading_statistic_repository = reading_statistic_repository

    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        return self.reading_statistic_repository.create_statistic_by_session(session)

    def add_total_reading_time_to_existing_statistic(self, session: Session,
                                                     statistic: ReadingStatistic) -> ReadingStatistic:
        return self.reading_statistic_repository.add_total_reading_time_to_existing_statistic(session, statistic)

    def get_all_statistics(self) -> ReadingStatistic:
        return self.reading_statistic_repository.get_all_statistics()

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        return self.reading_statistic_repository.get_all_statistics_by_visitor(visitor)

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        return self.reading_statistic_repository.get_statistic_by_visitor_and_book(visitor, book)

    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        return self.reading_statistic_repository.get_statistic_by_session(session)
