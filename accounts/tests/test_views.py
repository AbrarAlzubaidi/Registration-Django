from django.test import TestCase, Client
from django.contrib.auth.models import User

from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core import mail

from django.contrib.messages import get_messages
from accounts.forms import NewUserForm


### test register view
class RegisterViewTest(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'first_name': 'david',
            'last_name': 'calob',
            'username': 'david@123',
            'email': 'david@example.com',
            'password1': 'Test#12345',
            'password2': 'Test#12345'
        }

    def test_register_view_get_request(self):
        """
        test GET request for register view
        """
        client = Client()
        response = client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        # test that we use the NewUserForm for registration
        self.assertIsInstance(response.context['register_form'], NewUserForm)

    def test_register_view_post_request_with_valid_data(self):
        """
        test POST request for register view with valid data
        """
        client = Client()
        response = client.post(reverse('register'), RegisterViewTest.get_user_data())

        self.assertRedirects(response, reverse('home'))
        # test register successfully by check if the created user is in the database
        self.assertTrue(User.objects.filter(username=RegisterViewTest.get_user_data()['username']).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Registration is successful')

    def test_register_view_post_request_with_invalid_data(self):
        """
        test POST request for register view with invalid data
        """
        client = Client()
        # Provide invalid data to trigger form validation errors
        data = RegisterViewTest.get_user_data()
        data['email'] = 'exampletest.com'

        response = client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        # test that we use the NewUserForm for registration
        self.assertIsInstance(response.context['register_form'], NewUserForm)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), 'Email: Enter a valid email address.')
        self.assertEqual(str(messages[1]), 'Email: Invalid email format.')

### test login view
class LoginViewTest(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'username': 'david@123',
            'password': 'Test#12345',
        }

    def test_login_view_get_request(self):
        """
        test GET request for login view
        """
        client = Client()
        response = client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['login_form'](), AuthenticationForm)

    def test_login_view_post_request_with_valid_data(self):
        """
        test POST request for login view with valid data
        """
        test_user = User.objects.create_user(username=LoginViewTest.get_user_data()['username'], password=LoginViewTest.get_user_data()['password'])

        client = Client()
        response = client.post(reverse('login'), {'username': LoginViewTest.get_user_data()['username'], 'password': LoginViewTest.get_user_data()['password']}, follow=True)

        self.assertRedirects(response, reverse('home'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'logged in successfully')

    def test_login_view_post_request_with_invalid_data(self):
        """
        test POST request for login view with invalid data
        """
        client = Client()
        response = client.post(reverse('login'), {'username': LoginViewTest.get_user_data()['username'], 'password': 'Test@123'}, follow=True)

        self.assertTemplateUsed(response, 'accounts/login.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Password and/or username are wrong. Please enter the correct information')

### test logout view
class LogoutViewTest(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'username': 'david@123',
            'password': 'Test#12345',
        }
    
    def setUp(self):
        """
        setup new user credential
        """
        self.user = User.objects.create_user(username=LogoutViewTest.get_user_data()['username'], password=LogoutViewTest.get_user_data()['password'])

    def test_logout_view(self):
        """
        test logout view after user logged in
        """
        client = Client()
        logged_in = client.login(username=LogoutViewTest.get_user_data()['username'], password=LogoutViewTest.get_user_data()['password'])
        self.assertTrue(logged_in)

        response = client.get(reverse('logout'))

        self.assertRedirects(response, reverse('index'))

### test reset password view
class PasswordResetRequestTest(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'username': 'david@123',
            'email': 'david@example.com',
            'password': 'Test#12345',
        }
    
    def setUp(self):
        """
        setup new user credential
        """
        User.objects.create_user(username=PasswordResetRequestTest.get_user_data()['username'], email=PasswordResetRequestTest.get_user_data()['email'], password=PasswordResetRequestTest.get_user_data()['password'])

    def test_password_reset_request_with_valid_email(self):
        """
        test reset password view with valid email
        """
        client = Client()
        response = client.post(reverse('password_reset_request'), {'email': PasswordResetRequestTest.get_user_data()['email']})
        
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password Reset Request')

    def test_password_reset_request_with_invalid_email(self):
        """
        test reset password view with invalid email
        """
        client = Client()
        try:
            response = client.post(reverse('password_reset_request'), {'email': 'invalid@example.com'})
            self.assertRedirects(response, reverse('password_reset_request'))
        except User.DoesNotExist:
            self.assertEqual(len(mail.outbox), 0)

### test confirm reset password view
class PasswordResetConfirmTestCase(TestCase):
    @classmethod
    def get_user_data(cls):
        return {
            'username': 'david@123',
            'email': 'david@example.com',
            'password': 'Test#12345',
        }
    
    def setUp(self):
        """
        setup new user credential
        """
        self.user = User.objects.create_user(username=PasswordResetConfirmTestCase.get_user_data()['username'], email=PasswordResetConfirmTestCase.get_user_data()['email'], password=PasswordResetConfirmTestCase.get_user_data()['password'])
        self.token = default_token_generator.make_token(self.user)
        self.uidb64 = str(self.user.pk)

    def test_password_reset_confirm_get_request_with_valid_token(self):
        """
        test GET request for reset confirm view with valid token
        """
        client = Client()
        response = client.get(reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password-reset/password_reset_confirm.html')

    def test_password_reset_confirm_get_request_with_invalid_token(self):
        """
        test GET request for reset confirm view with invalid token
        """
        client = Client()
        invalid_token = 'hsdjhjahuiqdnjk'
        response = client.get(reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': invalid_token}))

        self.assertRedirects(response, reverse('password_reset_request'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'error')
        self.assertEqual(messages[0].message, 'Invalid reset link.')


    def test_password_reset_confirm_post_request_with_valid_token(self):
        """
        test POST request for reset confirm view with valid token
        """
        client = Client()
        new_password = 'Test@123'
        response = client.post(reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token}), {'new_password1': new_password, 'new_password2': new_password})

        self.assertRedirects(response, reverse('login'))

        # Check if user's password is updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))

    def test_password_reset_confirm_post_request_with_invalid_data(self):
        """
        test POST request for reset confirm view with invalid token
        """
        client = Client()
        invalid_data = {'new_password1': 'Test@123', 'new_password2': 'Test@12345'}
        try:
            client.post(reverse('password_reset_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token}), invalid_data)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            error_message = str(e)
            self.assertEqual(type(error_message), str )
        
### test password reset done view
class PasswordResetDoneTest(TestCase):
    def test_password_done_view(self):
        client = Client()
        response = client.get(reverse('password_reset_done'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password-reset/password_reset_done.html')
