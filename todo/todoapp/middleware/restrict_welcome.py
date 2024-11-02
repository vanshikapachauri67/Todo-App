# todo_app/middleware/restrict_welcome.py
from django.shortcuts import redirect
from django.urls import reverse

class RestrictWelcomePageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is authenticated and trying to access the welcome page
        if request.user.is_authenticated and request.path == reverse('welcome'):
            return redirect('home')  # Redirect to the home page
        return self.get_response(request)
