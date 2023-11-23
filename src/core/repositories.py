from dataclasses import dataclass
from itertools import repeat
from typing import Iterable

from auto_dataclass.dj_model_to_dataclass import ToDTOConverter
from django.db.models import Model

from core.interfaces import DTOConverterInterface


class DTOConverterRepository(DTOConverterInterface):
    def __init__(self, converter: ToDTOConverter):
        self.converter = converter

    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        return self.converter.to_dto(query, dto_class)

    def convert_many_to_dto(self, dto_class: dataclass, query: Iterable[Model]) -> Iterable[dataclass]:
        return map(self.converter.to_dto, query, repeat(dto_class))
