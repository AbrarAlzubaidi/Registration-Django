from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_view(request):
    """
    landing page when user navigates into the website
    that will return a http response
    """
    template_path = "home/index.html"
    return render(request, template_path, {"name": "Project"})


@login_required
def home_page_view(request):
    """
    home page view when user logged in
    """ 
    return render(request, "home/home.html")


def custom_permission_denied_403(request, exception):
    return render(request, 'errors_handler/403.html', status=403)

def custom_permission_denied_404(request, exception):
    print('=============')
    return render(request, 'errors_handler/404.html', status=404)