from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ActivityArea

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите вашу электронную почту',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите ваше имя',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите вашу фамилию',
    }))
    workplace = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите место работы',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите ваш телефон',
    }))
    position = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите вашу должность',
    }))
    activity_area = forms.ModelChoiceField(queryset=ActivityArea.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control form-control-lg',
    }), required=True)
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите вашу страну',
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите ваш город',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите пароль',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Подтвердите пароль',
    }))

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'password1', 'password2', 'workplace', 'phone',
            'position', 'activity_area', 'country', 'city'
        )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите вашу электронную почту',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Введите пароль',
    }))


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone', 'workplace', 'position',
            'activity_area', 'country', 'city', 'avatar'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_area': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'workplace': 'Место работы',
            'position': 'Должность',
            'activity_area': 'Сфера деятельности',
            'country': 'Страна',
            'city': 'Город',
            'avatar': 'Аватар',
        }
