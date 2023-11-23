from datetime import timedelta

from core.fixtures_for_tests import (create_statistic, create_book, get_access_for_base_user,
                                     open_session, close_session, create_session, create_user)

import pytest
from rest_framework.test import APIClient

client = APIClient()


def test_statistic_by_user(create_session, close_session, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    statistic = client.get('/api/v1/reading_statistics/visitor/', headers=headers)

    data = dict(statistic.data['statistic'][0])

    unexpected_time = timedelta(0)

    time = data['total_reading_time'].split(':')

    assert statistic.status_code == 200
    assert timedelta(hours=float(time[0]), minutes=float(time[1]), seconds=float(time[2])) > unexpected_time


def test_statistic_by_user_and_book(create_session, close_session, create_book, get_access_for_base_user):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    statistic = client.get(f'/api/v1/reading_statistics/books/{create_book.pk}/', headers=headers)

    data = statistic.data['statistic']

    book_data = dict(data['book'])

    unexpected_time = timedelta(0)

    time = data['total_reading_time'].split(':')

    assert statistic.status_code == 200
    assert book_data['id'] == create_book.id
    assert timedelta(hours=float(time[0]), minutes=float(time[1]), seconds=float(time[2])) > unexpected_time


def test_statistic_by_user_and_book_which_does_not_exist(
        create_session,
        close_session,
        get_access_for_base_user,
):
    access = get_access_for_base_user

    headers = dict(
        Authorization=f'Bearer {access}',
    )

    statistic = client.get('/api/v1/reading_statistics/books/999999/', headers=headers)
    expected = {'error': 'Book with id 999999 does not exist!'}

    assert statistic.status_code == 404
    assert expected == statistic.data


def test_all_statistic_by_book(create_book, open_session, close_session, create_statistic):
    statistic = client.get(f'/api/v1/reading_statistics/books_statistics/{create_book.pk}/')
    data = statistic.data['statistic']

    assert statistic.status_code == 200
    assert len(data) == 2


@pytest.mark.django_db
def test_all_statistic_by_book_which_does_not_exist():

    statistic = client.get('/api/v1/visitors/reading_statistics/books_statistics/999999/')

    expected = {'error': 'Book with id 999999 does not exist!'}

    assert statistic.status_code == 400
    assert expected == statistic.data


@pytest.mark.django_db
def test_all_statistic_by_book_which_does_not_exist(open_session, close_session, create_statistic):

    statistic = client.get('/api/v1/reading_statistics/')
    data = statistic.data['statistic']

    assert statistic.status_code == 200
    assert len(data) == 2
