import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db

@pytest.fixture
def create_user():
    User = get_user_model()
    User = User.objects.create_user(
        username='ernest',
        email='ernest@hevea.com',
        password='passme123',
    )
    return User

@pytest.fixture
def signup_page(client):
    signup_url = reverse('account_signup')
    signup_response = client.get(signup_url)
    return signup_response


class TestCustomUser:
    def test_username(self, create_user):
        user = create_user
        assert user.username == 'ernest'


    def test_user_email(self, create_user):
        user = create_user
        assert user.email == 'ernest@hevea.com'


    def test_user_is_active(self, create_user):
        user = create_user
        assert user.is_active is True


    def test_user_is_staff(self, create_user):
        user = create_user
        user.is_staff = True
        assert user.is_staff is True


    def test_user_is_superuser(self):
        user = get_user_model()
        admin_user = user.objects.create_superuser(
            username='admin',
            email='admin@hevea.com',
            password='passmeadmin',
        )
        assert admin_user.is_superuser is True

class TestSignUp:
    def test_signup_page(self, signup_page):
        assert signup_page.status_code == 200

    def test_signup_template(self, signup_page):
        assertTemplateUsed(signup_page, 'account/signup.html')

    def test_signup_content(self, signup_page):
        assert 'Sign Up' in str(signup_page.content)
        assert "I am not here" not in str(signup_page.content)

    def test_signup_form(self, signup_page):
        new_user = get_user_model().objects.create_user(username='iamuser', email='iamuser@email.com', password='passme123')
        assert new_user.username == 'iamuser'
        assert 'csrfmiddlewaretoken' in str(signup_page.content)



