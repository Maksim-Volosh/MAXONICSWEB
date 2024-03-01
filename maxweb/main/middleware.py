from django.shortcuts import redirect
from django.urls import reverse

UNPROTECTED_URLS = ['register', 'login', 'portfolio', 'home']

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = request.path

        if not request.user.is_authenticated and current_url not in [reverse(url) for url in UNPROTECTED_URLS]:
            request.session['desired_url'] = current_url
            return redirect('register')
        return self.get_response(request)
