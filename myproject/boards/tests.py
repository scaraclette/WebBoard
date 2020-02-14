from django.urls import reverse,resolve
from django.test import TestCase
from .views import home

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        # need to put slash on resolve('/') because it matches URL name rather than path resolve('')
        view = resolve('/')
        self.assertEquals(view.func, home)