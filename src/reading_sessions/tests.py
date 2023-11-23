from core.fixtures_for_tests import (create_user, create_book, create_another_book,
                                     get_access_for_base_user, open_session, close_session, create_session)

from rest_framework.test import APIClient

client = APIClient()


def test_open_session(open_session):
    session = open_session

    expected = {'message': 'Session has been successfully opened!'}

    assert expected.get('message') == session.get('message')


def test_open_session_book_does_not_exist_error(create_book, create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    session = client.post('/api/v1/sessions/open_session/999999/', headers=headers)

    expected = {'error': 'Book with id 999999 does not exist!'}

    assert expected == session.data


def test_open_session_book_is_already_taken_error(create_book, create_user, get_access_for_base_user, open_session):
    book = create_book
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    session = client.post(f'/api/v1/sessions/open_session/{book.pk}/', headers=headers)

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

    second_session = client.post(f'/api/v1/sessions/open_session/{another_book.pk}/', headers=headers)

    assert open_session['session']['book']['title'] != second_session.data['session']['book']['title']


def test_get_active_visitor_session(open_session, create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    current_session = client.get('/api/v1/sessions/current_session/', headers=headers)

    expected = 'session'

    assert expected in current_session.data.keys()


def test_get_session_session_does_not_exist(create_user, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    current_session = client.get('/api/v1/sessions/current_session/', headers=headers)

    expected = {'error': 'You have no active reading_sessions yet'}

    assert expected == current_session.data


def test_close_session(create_session, close_session):

    expected = {'message': 'Session has been successfully closed!'}

    assert close_session == expected


def test_close_session_which_does_not_exist(close_session):
    expected = {'error': 'You have no active reading_sessions yet'}

    assert close_session == expected
