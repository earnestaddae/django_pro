import pytest
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from pages.views import HomePageView, AboutPageView

@pytest.fixture
def home_resp(client):
    res = client.get('/')
    return res

@pytest.fixture
def about_resp(client):
    url = reverse('about')
    res = client.get(url)
    return res

class TestHomePage:
    def test_homepage_status_code(self, home_resp):
        assert home_resp.status_code == 200

    def test_homepage_url_name(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_homepage_template(self, home_resp):
        assertTemplateUsed(home_resp,'home.jinja')

    def test_homepage_contains_correct_html(self, home_resp):
        assert 'Homepage' in str(home_resp.content)

    def test_homepage_contains_incorrect_html(self, home_resp):
        assert "I am not here" not in str(home_resp.content)

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        assert view.func.__name__ == HomePageView.as_view().__name__

class TestAboutPage:
    def test_aboutpage_status_code(self, about_resp):
        assert about_resp.status_code == 200

    def test_aboutpage_template(self, about_resp):
        assertTemplateUsed(about_resp, 'about.jinja')

    def test_aboutpage_contains_correct_html(self, about_resp):
        assert 'About page' in str(about_resp.content)

    def test_aboutpage_contains_incorrect_html(self, home_resp):
        assert "I am not about page" not in str(home_resp.content)

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/about/')
        assert view.func.__name__ == AboutPageView.as_view().__name__

