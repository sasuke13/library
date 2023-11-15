from typing import Iterable

from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO
from visitors.interfaces import VisitorRepositoryInterface
from visitors.models import Visitor


class VisitorService(VisitorRepositoryInterface):
    def __init__(self, repository: VisitorRepositoryInterface):
        self.repository = repository

    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        return self.repository.registration(visitor_registration_dto)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        return self.repository.get_users_statistic_dto(visitor)
