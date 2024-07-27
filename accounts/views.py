from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('signin')

class SignInView(LoginView):
    template_name = 'registration/signin.html'
    success_url = reverse_lazy('map')

class SignOutView(LogoutView):
    next_page = reverse_lazy('map')
