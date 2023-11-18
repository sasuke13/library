from typing import Iterable

from books.interfaces import BookRepositoryAndServiceInterface
from books.models import Book
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.exceptions import SessionDoesNotExist, BookIsAlreadyTaken
from visitors.interfaces import VisitorRepositoryAndServiceInterface, VisitorInteractorInterface, \
    SessionRepositoryAndServiceInterface, SessionInteractorInterface, DTOConverterInterface, \
    ReadingStatisticRepositoryAndServiceInterface, ReadingStatisticInteractorInterface
from visitors.models import Visitor, Session, ReadingStatistic


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

    def add_total_reading_time_by_session(self, session: Session):
        self.visitor_service.add_total_reading_time_by_session(session)

    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        pass


class SessionInteractor(SessionInteractorInterface):
    def __init__(
            self,
            visitor_service: VisitorRepositoryAndServiceInterface,
            session_service: SessionRepositoryAndServiceInterface,
            book_service: BookRepositoryAndServiceInterface,
            reading_statistic_service: ReadingStatisticRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface
    ):
        self.visitor_service = visitor_service
        self.session_service = session_service
        self.book_service = book_service
        self.reading_statistic_service = reading_statistic_service
        self.converter_service = converter_service

    def get_active_session_dto_by_visitor(self, visitor: Visitor) -> SessionDTO:
        session = self.session_service.get_active_session_by_visitor(visitor)
        session_dto = self.converter_service.convert_to_dto(SessionDTO, session)

        return session_dto

    def get_all_sessions_dto_by_visitor(self, visitor: Visitor) -> Iterable[SessionDTO]:
        return self.session_service.get_all_sessions_dto_by_visitor(visitor)

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        return self.session_service.get_active_session_by_visitor(visitor)

    def get_active_session_by_book(self, book: Book) -> Session:
        return self.session_service.get_active_session_by_book(book)

    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        book = self.book_service.get_book_by_id(book_id)
        session_by_book = self.session_service.get_active_session_by_book(book)

        if session_by_book:
            raise BookIsAlreadyTaken()

        try:
            active_session = self.session_service.get_active_session_by_visitor(visitor)

            self.session_service.close_session(active_session)
            print('a')
            self.visitor_service.add_total_reading_time_by_session(active_session)

        except SessionDoesNotExist:
            ...
        return self.session_service.open_session(visitor, book)

    def close_session(self, visitor: Visitor) -> str:
        active_session = self.session_service.get_active_session_by_visitor(visitor)
        statistic = self.reading_statistic_service.get_statistic_by_session(active_session)

        message = self.session_service.close_session(active_session)

        self.visitor_service.add_total_reading_time_by_session(active_session)

        if statistic:
            self.reading_statistic_service.add_total_reading_time_to_existing_statistic(active_session, statistic)

        else:
            self.reading_statistic_service.create_statistic_by_session(active_session)

        return message


class ReadingStatisticInteractor(ReadingStatisticInteractorInterface):
    def __init__(
            self,
            reading_statistic_service: ReadingStatisticRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface
    ):
        self.reading_statistic_service = reading_statistic_service
        self.converter_service = converter_service

    def get_all_statistics_dto(self) -> Iterable[ReadingStatisticDTO]:
        statistics = self.reading_statistic_service.get_all_statistics()
        statistics_dto = self.converter_service.convert_many_to_dto(ReadingStatisticDTO, statistics)

        return statistics_dto

    def get_all_statistics_dto_by_visitor(self, visitor: Visitor) -> Iterable[ReadingStatistic]:
        statistics = self.reading_statistic_service.get_all_statistics_by_visitor(visitor)
        statistics_dto = self.converter_service.convert_many_to_dto(ReadingStatisticDTO, statistics)

        return statistics_dto

    def get_statistic_dto_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatisticDTO:
        statistic = self.reading_statistic_service.get_statistic_by_visitor_and_book(visitor, book)
        statistic_dto = self.converter_service.convert_to_dto(ReadingStatisticDTO, statistic)

        return statistic_dto

    def get_all_statistics(self) -> ReadingStatistic:
        statistics = self.reading_statistic_service.get_all_statistics()

        return statistics

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        statistics = self.reading_statistic_service.get_all_statistics_by_visitor(visitor)

        return statistics

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        statistic = self.reading_statistic_service.get_statistic_by_visitor_and_book(visitor, book)

        return statistic
