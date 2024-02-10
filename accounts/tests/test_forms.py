from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import NewUserForm, CustomPasswordResetForm

### test new user form
class NewUserFormTest(TestCase):
    @classmethod
    def get_user_form_data(cls):
        return {
            'first_name': 'david',
            'last_name': 'calob',
            'username': 'david@123',
            'email': 'david@example.com',
            'password1': 'Test#12345',
            'password2': 'Test#12345'
        }
    
    def test_valid_form(self):
        """
        test if passing a valid data
        """
        form = NewUserForm(data=NewUserFormTest.get_user_form_data())
        self.assertTrue(form.is_valid())

    def test_not_pass_firstname(self):
        """
        test if not passing firstname
        """
        form_data_without_firstname = NewUserFormTest.get_user_form_data()
        form_data_without_firstname['first_name'] = ''

        form = NewUserForm(data=form_data_without_firstname)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('first_name' in form.errors)
        self.assertEqual(form.errors['first_name'], ['This field is required.'])

    def test_not_pass_lastname(self):
        """
        test not passing lastname
        """
        form_data_without_lastname = NewUserFormTest.get_user_form_data()
        form_data_without_lastname['last_name'] = ''
        
        form = NewUserForm(data=form_data_without_lastname)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('last_name' in form.errors)
        self.assertEqual(form.errors['last_name'], ['This field is required.'])

    def test_not_pass_username(self):
        """
        test if not passing username
        """
        form_data_without_username = NewUserFormTest.get_user_form_data()
        form_data_without_username['username'] = ''
        
        form = NewUserForm(data=form_data_without_username)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('username' in form.errors)
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_not_pass_email(self):
        """
        test if not passing email
        """
        form_data_without_email = NewUserFormTest.get_user_form_data()
        form_data_without_email['email'] = ''
        
        form = NewUserForm(data=form_data_without_email)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('email' in form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_not_pass_password1(self):
            """
            test if not passing password1
            """
            form_data_without_password1 = NewUserFormTest.get_user_form_data()
            form_data_without_password1['password1'] = ''
            
            form = NewUserForm(data=form_data_without_password1)
            self.assertFalse(form.is_valid())
            
            self.assertTrue('password1' in form.errors)
            self.assertEqual(form.errors['password1'], ['This field is required.'])

    def test_not_pass_password2(self):
        """
        test if not passing password2
        """
        form_data_without_password2 = NewUserFormTest.get_user_form_data()
        form_data_without_password2['password2'] = ''
        
        form = NewUserForm(data=form_data_without_password2)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('password2' in form.errors)
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_firstname_more_than_10(self):
            """
            test if passing more than 10 letters in firstname
            """
            form_data_with_invalid_firstname = NewUserFormTest.get_user_form_data()
            form_data_with_invalid_firstname['first_name'] = 'firstname123'
            
            form = NewUserForm(data=form_data_with_invalid_firstname)
            self.assertFalse(form.is_valid())
            
            self.assertTrue('first_name' in form.errors)
            self.assertEqual(form.errors['first_name'], ['Ensure this value has at most 10 characters (it has 12).'])

    def test_lastname_more_than_10(self):
        """
        test if passing more than 10 letters in lastname
        """
        form_data_with_invalid_lastname = NewUserFormTest.get_user_form_data()
        form_data_with_invalid_lastname['last_name'] = 'lastname1234'
        
        form = NewUserForm(data=form_data_with_invalid_lastname)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('last_name' in form.errors)
        self.assertEqual(form.errors['last_name'], ['Ensure this value has at most 10 characters (it has 12).'])

    def test_username_more_than_20(self):
        """
        test if passing more than 20 letters in username
        """
        form_data_with_invalid_username = NewUserFormTest.get_user_form_data()
        form_data_with_invalid_username['username'] = 'username12345678901234'
        
        form = NewUserForm(data=form_data_with_invalid_username)
        self.assertFalse(form.is_valid())
        
        self.assertTrue('username' in form.errors)
        self.assertEqual(form.errors['username'], ['Username should be at most 20 characters long.'])

    def test_if_passwords_not_match(self):
        """
        test if the passwords not match
        """
        form_data = NewUserFormTest.get_user_form_data()
        form_data['password2'] = 'Example#123'

        form = NewUserForm(data=form_data)

        self.assertTrue('password2' in form.errors)
        self.assertTrue('Passwords do not match.' in form.errors['password2'])

    def test_invalid_email_format(self):
        """
        test if email has invalid format
        """
        form_data = NewUserFormTest.get_user_form_data()
        form_data['email'] = 'davidexample.com'

        form = NewUserForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)  
        self.assertTrue('Invalid email format.' in form.errors['email'])

    def test_save_method(self):
        """
        test the save method
        """
        form_data = NewUserFormTest.get_user_form_data()
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        
        self.assertIsInstance(user, User)
        self.assertEqual(user.first_name, form_data['first_name'])
        self.assertEqual(user.last_name, form_data['last_name'])
        self.assertEqual(user.username, form_data['username'])
        self.assertEqual(user.email, form_data['email'])

    def test_widget_attrs(self):
        """
        test the widget class property is exist
        """
        form = NewUserForm()

        self.assertEqual(form.fields["username"].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields["password1"].widget.attrs.get("class"), "form-control")
        self.assertEqual(form.fields["password2"].widget.attrs.get("class"), "form-control")


### test new user form
class CustomPasswordResetFormTest(TestCase):
    def test_widget_attrs(self):
        """
        test the widget class property is exist
        """
        form = CustomPasswordResetForm()

        self.assertEqual(form.fields["email"].widget.attrs.get("class"), "form-control")
