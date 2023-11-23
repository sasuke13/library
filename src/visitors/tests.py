import warnings

from core.fixtures_for_tests import (create_user, create_book, create_another_book,
                                     get_access_for_base_user, open_session, close_session, create_session)

import pytest
from rest_framework.test import APIClient

client = APIClient()


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
            'total_reading_time_for_the_last_week': '00:00:00',
            'total_reading_time_for_the_last_month': '00:00:00'
        }
    }

    response = client.post('/api/v1/visitors/registration/', payload)

    data = response.data

    assert data == expected


def test_login(create_user):
    login_credentials = dict(
        email='visitor@email.com',
        password='password1295'
    )

    response = client.post('/api/v1/visitors/login/', login_credentials)

    data = response.data

    assert client.cookies.get('refresh_token').value
    assert data.get('access')


def test_logout(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    expected = dict(
        message="User was successfully logged out"
    )

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    response = client.post('/api/v1/visitors/logout/', headers=headers)
    data = response.data

    assert data == expected
    assert not client.cookies.get('refresh_token').value


def test_logout_token_error(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    expected = dict(
        error='Refresh token not found'
    )

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    client.post('/api/v1/visitors/logout/', headers=headers)
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


def test_close_session(create_session, close_session):
    warnings.warn(UserWarning(create_session))
    warnings.warn(UserWarning(close_session))
    expected = {'message': 'Session has been successfully closed!'}

    assert close_session == expected


def test_close_session_which_does_not_exist(close_session):
    expected = {'error': 'You have no active sessions yet'}

    assert close_session == expected
