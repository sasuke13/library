from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from reading_sessions.models import Session
from visitors.dto import VisitorRegistrationDTO, VisitorDTO
from visitors.models import Visitor


class VisitorRepositoryAndServiceInterface(ABC):
    @abstractmethod
    def change_total_reading_time_for_the_last_week(self, visitor: Visitor):
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self, visitor: Visitor):
        pass

    @abstractmethod
    def get_all_visitors(self) -> Visitor:
        pass

    @abstractmethod
    def does_visitor_exist_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        pass

    @abstractmethod
    def add_total_reading_time_by_session(self, session: Session):
        pass


class VisitorInteractorInterface(ABC):
    @abstractmethod
    def change_total_reading_time_for_the_last_week(self):
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self):
        pass

    @abstractmethod
    def get_all_visitors(self) -> Visitor:
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        pass


class DTOConverterInterface(ABC):
    @abstractmethod
    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        pass

    @abstractmethod
    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        pass
