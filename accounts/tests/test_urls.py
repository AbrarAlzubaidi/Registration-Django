from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import (
    register_view,
    login_view,
    logout_view,
    password_reset_request,
    password_reset_confirm,
    password_reset_done
)

class TestUrls(SimpleTestCase):
    def test_register_endpoint(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register_view)

    def test_login_endpoint(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_endpoint(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_password_reset_request_endpoint(self):
        url = reverse('password_reset_request')
        self.assertEqual(resolve(url).func, password_reset_request)

    def test_password_reset_confirm_endpoint(self):
        url = reverse('password_reset_confirm', kwargs={'uidb64': 'uid', 'token': 'token'})
        self.assertEqual(resolve(url).func, password_reset_confirm)

    def test_password_reset_done_endpoint(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func, password_reset_done)
