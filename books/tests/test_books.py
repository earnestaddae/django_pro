import pytest
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from ..models import Book

pytestmark = pytest.mark.django_db

# Create your tests here.
@pytest.fixture
def create_book():
    book = Book.objects.create(
        title="The Denial of Death",
        author="Ernest Becker",
        price="98",
    )
    return book

class TestBook:
    def test_book_listing(self, create_book):
        assert create_book.title == 'The Denial of Death'
        assert create_book.author == 'Ernest Becker'
        assert create_book.price == '98'

    def test_book_list_view(self, client):
        response = client.get(reverse('book_list'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_list.jinja')

    def test_succesful_book_detail_view(self, client, create_book):
        response = client.get(create_book.get_absolute_url())
        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_detail.jinja')

    def test_unsucceful_book_detail_view(self, client):
        response = client.get('/books/4321')
        assert response.status_code == 404

