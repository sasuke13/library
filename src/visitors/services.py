from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from reading_sessions.models import Session
from visitors.dto import VisitorRegistrationDTO
from visitors.interfaces import VisitorRepositoryAndServiceInterface, DTOConverterInterface
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

    def add_total_reading_time_by_session(self, session: Session):
        self.visitor_repository.add_total_reading_time_by_session(session)


class DTOConverterService(DTOConverterInterface):
    def __init__(self, converter_repository: DTOConverterInterface):
        self.converter_repository = converter_repository

    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        return self.converter_repository.convert_to_dto(dto_class, query)

    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        return self.converter_repository.convert_many_to_dto(dto_class, query)
