from itertools import repeat
from typing import Iterable

from annoying.functions import get_object_or_None

from core.abstract_classes import AbstractRepository
from visitors.dto import ReadingStatisticDTO, VisitorRegistrationDTO, VisitorDTO
from visitors.interfaces import VisitorRepositoryInterface
from visitors.models import Visitor, ReadingStatistic


class VisitorRepository(VisitorRepositoryInterface, AbstractRepository):
    def registration(self, visitor_registration_dto: VisitorRegistrationDTO) -> VisitorDTO:
        registered_visitor = Visitor.objects.create_user(**visitor_registration_dto.__dict__)

        return self.converter.to_dto(registered_visitor, VisitorDTO)

    def get_users_statistic_dto(self, visitor: Visitor) -> Iterable[ReadingStatisticDTO]:
        statistics = ReadingStatistic.objects.select_related(
            'visitor',
            'book'
        ).filter(visitor=visitor)

        return map(self.converter.to_dto, statistics, repeat(ReadingStatisticDTO))
