from abc import ABC, abstractmethod
from typing import Iterable

from visitors.dto import VisitorRegistrationDTO, VisitorDTO, ReadingStatisticDTO
from visitors.models import Visitor


class VisitorRepositoryInterface(ABC):
    @abstractmethod
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        pass

    @abstractmethod
    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        pass
