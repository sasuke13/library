from datetime import datetime

from rest_framework.test import APIClient
import pytest

from books.models import Book
from reading_sessions.models import Session
from reading_statistics.models import ReadingStatistic
from visitors.models import Visitor

client = APIClient()


@pytest.fixture
def create_user(db) -> Visitor:
    visitor_dict = dict(
        name='Name',
        surname='Surname',
        email='visitor@email.com',
        password='password1295'
    )

    visitor = Visitor.objects.create_user(**visitor_dict)

    return visitor


@pytest.fixture
def create_book(db) -> Book:
    book_dict = dict(
        title='title',
        author='Author',
        year_of_publication=1930,
        short_about='short about',
        about='a bit longer about'
    )

    book = Book.objects.create(**book_dict)

    return book


@pytest.fixture
def create_another_book(db) -> Book:
    book_dict = dict(
        title='another book',
        author='Author',
        year_of_publication=1930,
        short_about='short about',
        about='a bit longer about'
    )

    book = Book.objects.create(**book_dict)

    return book


@pytest.fixture
def create_session(db, create_book, create_user) -> Session:
    session = Session.objects.create(
        visitor=create_user,
        book=create_book,
        session_start=datetime(2023, 11, 21)
    )

    return session


@pytest.fixture
def create_statistic(create_book, create_user) -> ReadingStatistic:
    statistic = ReadingStatistic.objects.create(book=create_book, visitor=create_user)

    return statistic


@pytest.fixture
def get_access_for_base_user():
    login_credentials = dict(
        email='visitor@email.com',
        password='password1295'
    )

    access = client.post('/api/v1/visitors/login/', login_credentials)

    return access.data.get('access')


@pytest.fixture
def open_session(create_book, create_user, get_access_for_base_user):
    book = create_book

    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    session = client.post(f'/api/v1/sessions/open_session/{book.pk}/', headers=headers)

    return session.data


@pytest.fixture
def close_session(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    message = client.post('/api/v1/sessions/current_session/close/', headers=headers)
    return message.data
