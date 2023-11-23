from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model

from core.interfaces import DTOConverterInterface


class DTOConverterService(DTOConverterInterface):
    def __init__(self, converter_repository: DTOConverterInterface):
        self.converter_repository = converter_repository

    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        return self.converter_repository.convert_to_dto(dto_class, query)

    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        return self.converter_repository.convert_many_to_dto(dto_class, query)
