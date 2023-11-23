from dataclasses import dataclass
from datetime import datetime

from books.dto import BookDTO, BookWithTotalReadingTimeDTO
from visitors.dto import VisitorDTO


@dataclass(frozen=True)
class ReadingStatisticDTO:
    book: BookDTO
    visitor: VisitorDTO
    total_reading_time: datetime.time


@dataclass(frozen=True)
class ReadingStatisticWithBookTotalReadingTimeDTO:
    book: BookWithTotalReadingTimeDTO
    visitor: VisitorDTO
    total_reading_time: datetime.time
