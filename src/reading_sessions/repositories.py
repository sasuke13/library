from datetime import datetime

from django.utils import timezone

from books.models import Book
from reading_sessions.exceptions import SessionDoesNotExist
from reading_sessions.interfaces import SessionRepositoryAndServiceInterface
from reading_sessions.models import Session
from visitors.models import Visitor


class SessionRepository(SessionRepositoryAndServiceInterface):
    def get_all_sessions(self) -> Session:
        sessions = (Session.objects.all().order_by('visitor', 'book').
                    prefetch_related('visitor', 'book').select_related('visitor', 'book'))

        return sessions

    def get_all_sessions_by_visitor(self, visitor: Visitor) -> Session:
        sessions = visitor.sessions.prefetch_related('visitor', 'book').select_related('visitor', 'book')

        return sessions

    def get_active_session_by_visitor(self, visitor: Visitor) -> Session:
        active_session = visitor.sessions.filter(is_active=True).all().first()

        if not active_session:
            raise SessionDoesNotExist()

        return active_session

    def get_active_session_by_book(self, book: Book) -> Session:
        active_session = book.sessions.filter(is_active=True).all().first()

        return active_session

    def open_session(self, visitor: Visitor, book: Book) -> Session:
        session = Session.objects.create(visitor=visitor, book=book)

        return session

    def close_session(self, session: Session) -> str:
        book = session.book

        session.is_active = False
        session.session_end = timezone.now()

        session.save()

        book.last_used = datetime.now()
        book.save()

        return 'Session has been successfully closed!'
