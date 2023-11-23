from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BookListViewDTO:
    id: int
    title: str
    author: str
    year_of_publication: int
    short_about: str


@dataclass(frozen=True)
class CreateBookDTO:
    title: str
    author: str
    year_of_publication: int
    short_about: str
    about: str


@dataclass(frozen=True)
class BookDTO:
    id: int
    title: str
    author: str
    year_of_publication: int
    short_about: str
    about: str
    last_used: datetime


@dataclass(frozen=True)
class BookWithTotalReadingTimeDTO:
    id: int
    title: str
    total_reading_time: datetime.time
