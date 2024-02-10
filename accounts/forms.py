from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class NewUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), validators=[EmailValidator(message='Invalid email format.')],required=True)
    first_name = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField()
    error_messages = {}

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields['password1'].widget.attrs.update({"class": "form-control"})
        self.fields['password2'].widget.attrs.update({"class": "form-control"})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 10:
            raise ValidationError('First name should be at most 10 characters long.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 10:
            raise ValidationError('Last name should be at most 10 characters long.')
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 20:
            raise ValidationError('Username should be at most 20 characters long.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address is already in use.')
        if '@' not in email:
            raise ValidationError('Invalid email format. Email must contain "@" symbol.')
        if not (email.endswith('.com') or email.endswith('.net')):
            raise ValidationError('Invalid email domain. Email must end with ".com" or ".net".')
        return email

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
    

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control"})

