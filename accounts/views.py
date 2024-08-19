from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser, LegalDocument


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.agreed_to_terms = form.cleaned_data.get('agree_to_terms')
        user.save()
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
        # Если логин или пароль неверны, будет отображено общее сообщение
        messages.error(self.request, 'Неверный логин или пароль. Попробуйте еще раз.')
        return self.render_to_response(self.get_context_data(form=form))


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


class DocumentDownloadView(DetailView):
    model = LegalDocument
    slug_field = 'title'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        document = self.get_object()
        return FileResponse(document.file, as_attachment=True)
