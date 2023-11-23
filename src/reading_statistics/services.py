from books.models import Book
from reading_statistics.interfaces import ReadingStatisticRepositoryAndServiceInterface
from reading_statistics.models import ReadingStatistic
from visitors.models import Visitor, Session


class ReadingStatisticService(ReadingStatisticRepositoryAndServiceInterface):
    def __init__(self, reading_statistic_repository: ReadingStatisticRepositoryAndServiceInterface):
        self.reading_statistic_repository = reading_statistic_repository

    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        return self.reading_statistic_repository.create_statistic_by_session(session)

    def add_total_reading_time_to_existing_statistic(self, session: Session,
                                                     statistic: ReadingStatistic) -> ReadingStatistic:
        return self.reading_statistic_repository.add_total_reading_time_to_existing_statistic(session, statistic)

    def get_all_statistics(self) -> ReadingStatistic:
        return self.reading_statistic_repository.get_all_statistics()

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        return self.reading_statistic_repository.get_all_statistics_by_visitor(visitor)

    def get_all_statistics_by_book(self, book: Book) -> ReadingStatistic:
        return self.reading_statistic_repository.get_all_statistics_by_book(book)

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        return self.reading_statistic_repository.get_statistic_by_visitor_and_book(visitor, book)

    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        return self.reading_statistic_repository.get_statistic_by_session(session)
