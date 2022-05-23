import pytest
from django.urls import reverse, resolve
from pytest_django.asserts import assertTemplateUsed
from pages.views import HomePageView

# Create your tests here.
class TestHomePage:
    @pytest.fixture()
    def resp(self, client):
        res = client.get('/')
        return res


    def test_homepage_status_code(self, resp):
        assert resp.status_code == 200


    def test_homepage_url_name(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200


    def test_homepage_template(self, resp):
        assertTemplateUsed(resp,'home.jinja')


    def test_homepage_contains_correct_html(self, resp):
        assert 'Homepage' in str(resp.content)


    def test_homepage_contains_incorrect_html(self, resp):
        assert "I am not here" not in str(resp.content)


    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        assert view.func.__name__ == HomePageView.as_view().__name__
