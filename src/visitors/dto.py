import datetime
from dataclasses import dataclass


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
