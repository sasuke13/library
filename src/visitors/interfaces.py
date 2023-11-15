from abc import ABC, abstractmethod

from visitors.dto import VisitorRegistrationDTO


class VisitorRepositoryInterface(ABC):
    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO):
        pass
