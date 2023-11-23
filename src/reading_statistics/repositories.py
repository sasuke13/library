from books.models import Book
from reading_statistics.exceptions import StatisticDoesNotExist
from reading_statistics.interfaces import ReadingStatisticRepositoryAndServiceInterface
from reading_statistics.models import ReadingStatistic
from visitors.models import Visitor, Session


class ReadingStatisticRepository(ReadingStatisticRepositoryAndServiceInterface):

    def create_statistic_by_session(self, session: Session) -> ReadingStatistic:
        statistic = ReadingStatistic.objects.create(
            book=session.book,
            visitor=session.visitor,
        )

        return statistic

    def add_total_reading_time_to_existing_statistic(
            self,
            session: Session,
            statistic: ReadingStatistic
    ) -> ReadingStatistic:
        session_start = session.session_start
        session_end = session.session_end

        total_reading_time = session_end - session_start

        statistic.total_reading_time = statistic.total_reading_time + total_reading_time

        statistic.save()

        return statistic

    def get_all_statistics(self) -> ReadingStatistic:
        return (ReadingStatistic.objects.all().order_by('visitor', 'book').
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_all_statistics_by_visitor(self, visitor: Visitor) -> ReadingStatistic:
        return (visitor.statistics.all().
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_all_statistics_by_book(self, book: Book) -> ReadingStatistic:
        return (book.statistics.all().
                prefetch_related('book', 'visitor').
                select_related('book', 'visitor'))

    def get_statistic_by_visitor_and_book(self, visitor: Visitor, book: Book) -> ReadingStatistic:
        statistic = visitor.statistics.filter(book=book).first()

        if not statistic:
            raise StatisticDoesNotExist(f'You have no statistics for book with id {book.id}')

        return statistic

    def get_statistic_by_session(self, session: Session) -> ReadingStatistic:
        statistic = session.visitor.statistics.filter(book=session.book).first()

        return statistic
