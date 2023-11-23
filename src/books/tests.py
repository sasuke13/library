import warnings
from core.fixtures_for_tests import create_book, create_another_book
import pytest
from rest_framework.test import APIClient

client = APIClient()

book_data = dict(
    title="title",
    author="author",
    year_of_publication=2023,
    short_about="short",
    about="a bit longer about"
)


def test_get_all_books(create_book, create_another_book):
    response = client.get('/api/v1/books/')

    data = response.data

    assert response.status_code == 200
    assert len(data['book']) == 2


def test_get_book_by_id(create_book):
    response = client.get(f'/api/v1/books/{create_book.pk}/')

    data = response.data['book']

    assert response.status_code == 200
    assert data['id'] == create_book.pk


@pytest.mark.django_db
def test_get_book_which_does_not_exist():
    response = client.get('/api/v1/books/999999/')

    expected = {'error': 'Book with id 999999 does not exist!'}

    assert response.status_code == 404
    assert expected == response.data


@pytest.mark.django_db
def test_create_book():
    response = client.post('/api/v1/books/', book_data)

    data = response.data

    expected = {
        'message': 'Book was successfully created!',
        'book': {
            'id': 4,
            'title': 'title',
            'author': 'author',
            'year_of_publication': 2023,
            'short_about': 'short',
            'about': 'a bit longer about',
            'last_used': None
        }
    }

    assert response.status_code == 201
    assert expected == data


@pytest.mark.django_db
def test_create_book_unacceptable_value_for_year_of_publication():
    wrong_book_data = book_data
    wrong_book_data['year_of_publication'] = -1

    response = client.post('/api/v1/books/', wrong_book_data)

    data = response.data

    expected = 'Invalid year of publication'

    assert response.status_code == 400
    assert expected == data['errors']['non_field_errors'][0]
