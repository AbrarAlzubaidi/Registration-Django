from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from accounts.models import CustomUser

class CustomUserModelTest(TestCase):

    @classmethod
    def get_user_data(cls):
        return {
            'username' : 'test',
            'email' : 'test@example.com',
            'password' : 'test@123',
        }
    
    def setUp(self):
        """
        setup new user credential
        """
        test_user = User.objects.create_user(username=CustomUserModelTest.get_user_data()['username'], email=CustomUserModelTest.get_user_data()['email'], password=CustomUserModelTest.get_user_data()['password'])
        CustomUser.objects.create(user=test_user, email=CustomUserModelTest.get_user_data()['email'], username=CustomUserModelTest.get_user_data()['username'])

    def test_create_custom_user(self):
        """
        test create a user correctly
        """
        # find the user
        custom_user = CustomUser.objects.get(username=CustomUserModelTest.get_user_data()['username'])
        # return object if it is created successfully 
        self.assertIsNotNone(custom_user)
        
        # test created user attribute     
        self.assertEqual(custom_user.email, CustomUserModelTest.get_user_data()['email'])
        self.assertEqual(custom_user.username, CustomUserModelTest.get_user_data()['username'])

    def test_custom_user_str_method(self):
        """
        test the __str__ method: should return the username
        """
        # find the user
        custom_user = CustomUser.objects.get(username=CustomUserModelTest.get_user_data()['username'])
        
        self.assertEqual(str(custom_user), CustomUserModelTest.get_user_data()['username'])

    def test_username_not_unique(self):
        """
        test if username is already exist
        """

        with self.assertRaises(IntegrityError) as context:
            User.objects.create_user(username=CustomUserModelTest.get_user_data()['username'], email='another@example.com', password='anotherpassword')

        error_message = str(context.exception)
        self.assertIn('unique constraint', error_message.lower())
        self.assertIn('username', error_message.lower())

    def test_email_not_unique(self):
        """
        test if email is already exist
        """
        try:
            User.objects.create_user(username='test2', email=CustomUserModelTest.get_user_data()['email'], password='anotherpassword')
        except IntegrityError as e:
            error_message = str(e)
            self.assertIn('unique constraint', error_message.lower())
            self.assertIn('email', error_message.lower())




