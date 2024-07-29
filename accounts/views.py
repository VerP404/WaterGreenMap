from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"{field.label}: {error}")
        return super().form_invalid(form)


class SignInView(LoginView):
    template_name = 'registration/signin.html'
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        messages.success(self.request, 'Авторизация прошла успешно!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"{field.label}: {error}")
        return super().form_invalid(form)


class SignOutView(LogoutView):
    next_page = reverse_lazy('map')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
