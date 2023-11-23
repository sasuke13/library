from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Model


class DTOConverterInterface(ABC):
    @abstractmethod
    def convert_to_dto(self, dto_class: dataclass, query: Model) -> dataclass:
        """
        Converts 1 query into dto class.
        :param dto_class:
        :param query:
        :return Converted query's fields into the dto_class:
        """
        pass

    @abstractmethod
    def convert_many_to_dto(self, dto_class: dataclass, query: Model) -> Iterable[dataclass]:
        """
        Converts query with many instances into dto class.
        :param dto_class:
        :param query:
        :return Converted iterable query's fields into the dto_class:
        """
        pass
