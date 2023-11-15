from dataclasses import dataclass


@dataclass(frozen=True)
class BookDTO:
    title: str
    author: str
    year_of_publication: int
    short_about: str
    about: str
