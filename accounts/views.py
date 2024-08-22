from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import FileResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser, LegalDocument
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.views import View

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Деактивируем пользователя до подтверждения email
        user.save()
        user.send_confirmation_email(self.request)
        messages.success(self.request, 'Регистрация прошла успешно! Проверьте ваш email для подтверждения.')
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


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.confirm_email()
            messages.success(request, 'Ваш email подтвержден!')
            return redirect('signin')
        else:
            messages.error(request, 'Ссылка для подтверждения недействительна.')
            return redirect('signup')
