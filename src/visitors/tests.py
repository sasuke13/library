import warnings

from core.fixtures_for_tests import (create_user, get_access_for_base_user)

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

    warnings.warn(UserWarning(response.data))
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
