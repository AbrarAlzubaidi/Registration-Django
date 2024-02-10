from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import NewUserForm, CustomPasswordResetForm
from home.views import home_page_view, index_view

def login_view(request):
    """
    login view has 2 requests, one is the get request and when it happens:
            then we will render the form
        the second one when the post request happens
            then we will pass the data 
    """
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully')
                return redirect(home_page_view)
        else:
          messages.error(request, 'Password and/or username are wrong. Please enter the correct information')  
    elif request.method == 'GET':
        login_form = AuthenticationForm
    return render(request, 'accounts/login.html', {'login_form': login_form})


def register_view(request):
    """
    register view is to register/create new user/s in the application
    """
    if request.method == 'POST':
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Registration is successful')
            return redirect(home_page_view)
        else:
            # if any validation error happen it will be displayed to the user
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return render(request, 'accounts/register.html', {'register_form': register_form})
    else:
        register_form = NewUserForm()

    return render(request, 'accounts/register.html', {'register_form': register_form})


@login_required
def logout_view(request):
    """
    logged out the user from the system  
    """
    logout(request)
    return redirect(index_view)

def password_reset_request(request):
    """
    to reset the password if the user forget it by sending email of the confirm link for the user
    users should enter only their email 
    """
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)

            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': token}))
            try:
                send_mail(
                    'Password Reset Request',
                    f'Click the link below to reset your password:\n\n{reset_url}',
                    'contact@infinite.com',
                    [email],
                    fail_silently=True
                )
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'info': e
                })
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'password-reset/password_reset_request.html', {'form': form})


def password_reset_confirm(request, uidb64, token):
    """
    after the user receive the email from forget password button and check their is no error and authenticated
      it will redirect him/her into the changing password page
    """

    try:
        user = User.objects.get(pk=uidb64)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            return render(request, 'password-reset/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('password_reset_request')
    
def password_reset_done(request):
    """
    small view to show the user that the email is sent
    """
    return render(request, 'password-reset/password_reset_done.html')