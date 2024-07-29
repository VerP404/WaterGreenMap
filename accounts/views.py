from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class SignInView(LoginView):
    template_name = 'registration/signin.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('map')

class SignOutView(LogoutView):
    next_page = reverse_lazy('map')
