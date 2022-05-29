import pytest
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from ..models import Book, Review

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

@pytest.fixture
def create_review(create_book):
    user = get_user_model().objects.create_user(
        username='reviewer',
        email='reviewer@email.com',
        password='passme123',
    )

    special_permission = Permission.objects.get(codename='special_status')

    review = Review.objects.create(
        book = create_book,
        author = user,
        review='I am reviewed',
    )
    return review

class TestBook:
    def test_book_listing(self, create_book):
        assert create_book.title == 'The Denial of Death'
        assert create_book.author == 'Ernest Becker'
        assert create_book.price == '98'

    def test_book_list_view_for_logged_in_user(self, client, create_review):
        client.login(email=create_review.author.email, password=create_review.author.password)
        response = client.get(reverse('book_list'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_list.jinja')

    def test_succesful_book_detail_view(self, client, create_book, create_review):
        response = client.get(create_book.get_absolute_url())
        assert response.status_code == 200
        assertTemplateUsed(response, 'books/book_detail.jinja')
        assert create_review.book == create_book
        assert create_review.author.username == 'reviewer'

    def test_unsucceful_book_detail_view(self, client):
        response = client.get('/books/4321')
        assert response.status_code == 404

