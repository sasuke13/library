from visitors.dto import VisitorRegistrationDTO
from visitors.interfaces import VisitorRepositoryAndServiceInterface
from visitors.models import Visitor


class VisitorService(VisitorRepositoryAndServiceInterface):
    def __init__(self, visitor_repository: VisitorRepositoryAndServiceInterface):
        self.visitor_repository = visitor_repository

    def change_total_reading_time_for_the_last_week(self, visitor: Visitor):
        self.visitor_repository.change_total_reading_time_for_the_last_week(visitor)

    def change_total_reading_time_for_the_last_month(self, visitor: Visitor):
        self.visitor_repository.change_total_reading_time_for_the_last_month(visitor)

    def get_all_visitors(self) -> Visitor:
        return self.visitor_repository.get_all_visitors()

    def does_visitor_exist_by_email(self, email: str) -> bool:
        return self.visitor_repository.does_visitor_exist_by_email(email)

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        return self.visitor_repository.registration(visitor_registration_dto)
