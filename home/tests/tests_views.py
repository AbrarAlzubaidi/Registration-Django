from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

### test index page view
class IndexTest(TestCase):
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

### test home page view
class HomePageTest(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'username': 'david@123',
            'password': 'Test#12345',
            'email': 'david@example.com',
        }
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username=HomePageTest.get_user_data()['username'], email=HomePageTest.get_user_data()['email'], password=HomePageTest.get_user_data()['password'])
        self.client.login(username=HomePageTest.get_user_data()['username'], password=HomePageTest.get_user_data()['password'])

    def test_home_view_without_logged_in(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "login/?next=/home")

    def test_home_view_with_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        

