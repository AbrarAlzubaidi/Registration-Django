from django.urls import path
from .views import login_view, register_view, logout_view, password_reset_request, password_reset_confirm, password_reset_done

urlpatterns = [
    path("login", login_view, name='login'),
    path("register", register_view, name='register'),
    path("logout", logout_view, name='logout'),
    path('password-reset/', password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password-reset-done', password_reset_done, name='password_reset_done'),
]