from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from home.views import home_page_view, index_view
# Create your views here.
def login_view(request):
    """
    login view has 2 requests, one is the get method and when it happens:
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
            print('the authenticated user is: ', user)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in successfully')
                return redirect(home_page_view)
            else:
                # if the user not saved in the database then the user should be created 
                # a new account (register)
                # then redirect him/her into login page
                messages.error(request, 'unfortunately we cant see ur name with us try to register')
        else:
          messages.error(request, 'unfortunately we cant see u with us')  
    elif request.method == 'GET':
        login_form = AuthenticationForm
    return render(request, 'accounts/login.html', {'login_form': login_form})



def register_view(request):
    register_form = NewUserForm()
    if request.method == 'POST':
       register_form = NewUserForm(request.POST)
       if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Registration is successfully')
            return redirect(home_page_view)
    form = NewUserForm()
    return render(request, 'accounts/register.html', {'register_form':register_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect(index_view)