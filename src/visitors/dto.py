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
    password: str
    name: str
    surname: str
    total_reading_time: datetime.time


@dataclass(frozen=True)
class SessionDTO:
    book: BookDTO
    visitor: VisitorDTO
    session_start: datetime
    session_end: datetime
    is_active: bool
