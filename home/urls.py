from django.urls import path


from .views import (
    index_view, 
    home_page_view, 
    )

urlpatterns = [
    path("", index_view, name='index'),
    path('home', home_page_view, name='home'),
]