from reading_sessions.interfaces import SessionRepositoryAndServiceInterface
from visitors.dto import VisitorRegistrationDTO, VisitorDTO
from visitors.interfaces import VisitorRepositoryAndServiceInterface, VisitorInteractorInterface, DTOConverterInterface


class VisitorInteractor(VisitorInteractorInterface):
    def __init__(
            self,
            visitor_service: VisitorRepositoryAndServiceInterface,
            converter_service: DTOConverterInterface,
            session_service: SessionRepositoryAndServiceInterface,
    ):
        self.visitor_service = visitor_service
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

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        self.visitor_service.does_visitor_exist_by_email(visitor_registration_dto.email)

        visitor = self.visitor_service.registration(visitor_registration_dto)

        return self.converter_service.convert_to_dto(VisitorDTO, visitor)
