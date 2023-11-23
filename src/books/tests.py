import warnings
from core.fixtures_for_tests import create_book, create_another_book
import pytest
from rest_framework.test import APIClient

client = APIClient()


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
