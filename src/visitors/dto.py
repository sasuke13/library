import datetime
from dataclasses import dataclass

from books.dto import BookDTO


@dataclass(frozen=True)
class VisitorRegistrationDTO:
    email: str
    password: str
    name: str
    surname: str


@dataclass(frozen=True)
class VisitorDTO:
    email: str
    name: str
    surname: str
    total_reading_time_for_the_last_week: datetime.time
    total_reading_time_for_the_last_month: datetime.time


@dataclass(frozen=True)
class ReadingStatisticDTO:
    book: BookDTO
    visitor: VisitorDTO
    total_reading_time: datetime.time
