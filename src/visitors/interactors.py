from typing import Iterable

from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO
from visitors.interfaces import VisitorRepositoryInterface
from visitors.models import Visitor


class VisitorInteractor(VisitorRepositoryInterface):
    def __init__(self, service: VisitorRepositoryInterface):
        self.service = service

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        return self.service.registration(visitor_registration_dto)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        return self.service.get_users_statistic_dto(visitor)
