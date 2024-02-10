from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import (
    index_view,
    home_page_view,
)

class TestUrls(SimpleTestCase):
    def test_index_endpoint(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index_view)

    def test_home_page_endpoint(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home_page_view)

