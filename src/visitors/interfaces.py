from abc import ABC, abstractmethod

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
    def get_all_visitors_by_range_of_session_end(self, days: int) -> Visitor:
        """
        Makes query to get visitors by session_end in range between
        the current date and the week before, and is_active=False
        :param days:
        :return Visitor instance:
        """
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
        """
        Gets visitors with inactive sessions in range of week.
        Runs around the visitor query and
        subtracts total_reading_time_for_the_last_week with
        duration of all the inactive sessions in range of week.
        :return nothing:
        """
        pass

    @abstractmethod
    def change_total_reading_time_for_the_last_month(self):
        """
        Gets visitors with inactive sessions in range of month.
        Runs around the visitor query and
        subtracts total_reading_time_for_the_last_month with
        duration of all the inactive sessions in range of month.
        :return nothing:
        """
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
