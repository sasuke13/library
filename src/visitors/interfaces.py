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
        """
        Sets subtracted time of session durations in range of the last week of reading
        to visitor's total_reading_time_for_the_last_week field

        :param visitor:
        :return nothing:
        """
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self, visitor: Visitor):
        """
        Sets subtracted time of session durations in range of the last month of reading
        to visitor's total_reading_time_for_the_last_month field

        :param visitor:
        :return nothing:
        """
        pass

    @abstractmethod
    def get_all_visitors(self) -> Visitor:
        pass

    @abstractmethod
    def does_visitor_exist_by_email(self, email: str) -> bool:
        """
        Checks whether email is taken

        :param email:
        :return False(does not exist) or raises the VisitorAlreadyExists error(email is taken):
        """
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> Visitor:
        """
        Calls Visitor's create_user method to create Visitor instance.

        :param visitor_registration_dto:
        :return Visitor instance:
        """
        pass


class VisitorInteractorInterface(ABC):
    @abstractmethod
    def change_total_reading_time_for_the_last_week(self):
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self):
        pass

    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        """
        Checks whether email is taken.

        Registers the user.

        Converts gotten Visitor instance into VisitorDTO
        :param visitor_registration_dto:
        :return packed Visitor instance's fields in VisitorDTO:
        """
        pass
