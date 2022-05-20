import pytest
from django.contrib.auth import get_user_model


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
