from books.interfaces import BookRepositoryAndServiceInterface
from reading_statistics.interfaces import ReadingStatisticRepositoryAndServiceInterface
from visitors.dto import VisitorRegistrationDTO, VisitorDTO, SessionDTO
from visitors.exceptions import SessionDoesNotExist, BookIsAlreadyTaken
from visitors.interfaces import VisitorRepositoryAndServiceInterface, VisitorInteractorInterface, \
    SessionRepositoryAndServiceInterface, SessionInteractorInterface, DTOConverterInterface
from visitors.models import Visitor


class VisitorInteractor(VisitorInteractorInterface):
    def __init__(
            self,
            visitor_service: VisitorRepositoryAndServiceInterface,
            book_service: BookRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface,
            session_service: SessionRepositoryAndServiceInterface,
    ):
        self.visitor_service = visitor_service
        self.book_service = book_service
        self.converter_service = converter_service
        self.session_service = session_service

    def change_total_reading_time_for_the_last_week(self):
        visitors = self.visitor_service.get_all_visitors()
        visitors_list = []

        for visitor in visitors:
            if visitor not in visitors_list:
                self.visitor_service.change_total_reading_time_for_the_last_week(visitor)
                visitors_list.append(visitor)

    def change_total_reading_time_for_the_last_month(self):
        visitors = self.visitor_service.get_all_visitors()
        visitors_list = []

        for visitor in visitors:
            if visitor not in visitors_list:
                self.visitor_service.change_total_reading_time_for_the_last_month(visitor)
                visitors_list.append(visitor)

    def get_all_visitors(self) -> Visitor:
        return self.visitor_service.get_all_visitors()

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        self.visitor_service.does_visitor_exist_by_email(visitor_registration_dto.email)

        visitor = self.visitor_service.registration(visitor_registration_dto)

        return self.converter_service.convert_to_dto(VisitorDTO, visitor)


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

    def open_session(self, visitor: Visitor, book_id: int) -> SessionDTO:
        book = self.book_service.get_book_by_id(book_id)
        session_by_book = self.session_service.get_active_session_by_book(book)

        if session_by_book:
            raise BookIsAlreadyTaken()

        try:
            active_session = self.session_service.get_active_session_by_visitor(visitor)

            self.session_service.close_session(active_session)
            self.visitor_service.add_total_reading_time_by_session(active_session)

        except SessionDoesNotExist:
            ...

        session = self.session_service.open_session(visitor, book)

        return self.converter_service.convert_to_dto(SessionDTO, session)

    def close_session(self, visitor: Visitor) -> str:
        active_session = self.session_service.get_active_session_by_visitor(visitor)
        statistic = self.reading_statistic_service.get_statistic_by_session(active_session)

        message = self.session_service.close_session(active_session)

        self.visitor_service.add_total_reading_time_by_session(active_session)

        if not statistic:
            statistic = self.reading_statistic_service.create_statistic_by_session(session=active_session)

        self.reading_statistic_service.add_total_reading_time_to_existing_statistic(active_session, statistic)

        return message
