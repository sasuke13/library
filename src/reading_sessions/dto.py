from dataclasses import dataclass
from datetime import datetime

from books.dto import BookDTO
from visitors.dto import VisitorDTO


@dataclass(frozen=True)
class SessionDTO:
    book: BookDTO
    visitor: VisitorDTO
    session_start: datetime
    session_end: datetime
    is_active: bool
