from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ActivityArea(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    workplace = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    activity_area = models.ForeignKey(ActivityArea, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    registration_date = models.DateTimeField(default=timezone.now)
    auto_publish = models.BooleanField(default=False)
    agreed_to_terms = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError('Только файлы PDF допустимы.')


class LegalDocument(models.Model):
    DOCUMENT_CHOICES = [
        ('privacy_policy', 'Политика обработки персональных данных'),
        ('terms_of_service', 'Условия использования'),
    ]

    title = models.CharField(max_length=255, choices=DOCUMENT_CHOICES, verbose_name="Тип документа")
    version = models.CharField(max_length=50, verbose_name="Версия документа")
    file = models.FileField(upload_to='documents/', validators=[validate_pdf], verbose_name="Файл документа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        unique_together = ('title', 'version')

    def save(self, *args, **kwargs):
        if self.file:
            original_name = self.file.name
            extension = original_name.split('.')[-1]
            new_name = f"{self.get_title_display()}_{self.version}.{extension}"
            self.file.name = new_name

            # Проверка уникальности файла
            if LegalDocument.objects.filter(file=self.file.name).exists():
                raise ValidationError('Файл с такой версии существует!')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_title_display()} (Версия: {self.version})"
