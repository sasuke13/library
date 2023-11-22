import pytest
from rest_framework.test import APIClient

from books.models import Book
from visitors.models import Visitor, Session

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
    session = Session.objects.create(visitor=create_user, book=create_book)

    return session


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

    session = client.post(f'/api/v1/visitors/open_session/{book.pk}/', headers=headers)

    return session.data


@pytest.fixture
def close_session(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    message = client.post('/api/v1/visitors/current_session/close/', headers=headers)

    return message.data


@pytest.mark.django_db
def test_registration():
    payload = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='password1295'
    )

    expected = {
        'created_user': {
            'email': 'email@email.com',
            'name': 'Name',
            'surname': 'Surname',
            'total_reading_time': '00:00:00'
        }
    }

    response = client.post('/api/v1/visitors/registration/', payload)

    data = response.data

    assert data == expected


@pytest.mark.django_db
def test_login():
    payload = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='password1295'
    )

    login_credentials = dict(
        email='email@email.com',
        password='password1295'
    )

    client.post('/api/v1/visitors/registration/', payload)

    response = client.post('/api/v1/visitors/login/', login_credentials)

    data = response.data

    assert client.cookies.get('refresh_token').value
    assert data.get('access')


@pytest.mark.django_db
def test_logout():
    payload = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='password1295'
    )

    login_credentials = dict(
        email='email@email.com',
        password='password1295'
    )

    expected = dict(
        message="User was successfully logged out"
    )

    client.post('/api/v1/visitors/registration/', payload)

    logged_user = client.post('/api/v1/visitors/login/', login_credentials)

    headers = dict(
        Authorization=f'Bearer {logged_user.data.get("access")}',
    )

    response = client.post('/api/v1/visitors/logout/', headers=headers)

    data = response.data

    assert data == expected
    assert not client.cookies.get('refresh_token').value


@pytest.mark.django_db
def test_invalid_password_registration():
    payload = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='pass'  # too short
    )

    expected = {'error': 'This password is too short. '
                         'It must contain at least 8 characters.This password is too common.'}

    response = client.post('/api/v1/visitors/registration/', payload)

    data = response.data

    assert data == expected


@pytest.mark.django_db
def test_same_email_error_registration():
    first_user = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='password1295'
    )

    duplicated_user = dict(
        name='Name',
        surname='Surname',
        email='email@email.com',
        password='password1295'
    )

    expected = {'error': 'Visitor with email email@email.com already exists!'}

    client.post('/api/v1/visitors/registration/', first_user)

    response = client.post('/api/v1/visitors/registration/', duplicated_user)

    data = response.data

    assert data == expected


def test_open_session(open_session):
    session = open_session

    expected = {'message': 'Session has been successfully opened!'}

    assert expected.get('message') == session.get('message')


def test_open_session_book_does_not_exist_error(create_book, create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    session = client.post('/api/v1/visitors/open_session/999999/', headers=headers)

    expected = {'error': 'Book with id 999999 does not exist!'}

    assert expected == session.data


def test_open_session_book_is_already_taken_error(create_book, create_user, get_access_for_base_user, open_session):
    book = create_book
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    session = client.post(f'/api/v1/visitors/open_session/{book.pk}/', headers=headers)

    expected = {'error': 'This book is already taken'}

    assert expected == session.data


def test_open_session_and_open_another(
        create_book,
        create_another_book,
        create_user,
        get_access_for_base_user,
        open_session
):
    another_book = create_another_book
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    second_session = client.post(f'/api/v1/visitors/open_session/{another_book.pk}/', headers=headers)

    assert open_session['session']['book']['title'] != second_session.data['session']['book']['title']


def test_get_active_visitor_session(open_session, create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    current_session = client.get('/api/v1/visitors/current_session/', headers=headers)

    expected = 'session'

    assert expected in current_session.data.keys()


def test_get_session_session_does_not_exist(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    current_session = client.get('/api/v1/visitors/current_session/', headers=headers)

    expected = {'error': 'You have no active sessions yet'}

    assert expected == current_session.data


def test_close_session(open_session, close_session):
    expected = {'message': 'Session has been successfully closed!'}

    assert close_session == expected


def test_close_session_which_does_not_exist(close_session):
    expected = {'error': 'You have no active sessions yet'}

    assert close_session == expected
