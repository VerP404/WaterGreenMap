import os
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    color = models.CharField(max_length=7, verbose_name="Цвет")  # HEX color code
    icon = models.CharField(max_length=50, default="archive", verbose_name="Иконка")  # Имя иконки

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Type(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название типа")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    color = models.CharField(max_length=7, verbose_name="Цвет")  # HEX color code
    category = models.ForeignKey(Category, related_name='types', on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    main_type = models.ForeignKey(Type, related_name='main_projects', on_delete=models.CASCADE,
                                  verbose_name="Основной тип")
    additional_type_1 = models.ForeignKey(Type, related_name='additional_projects_1', on_delete=models.CASCADE,
                                          null=True, blank=True, verbose_name="Дополнительный тип 1")
    additional_type_2 = models.ForeignKey(Type, related_name='additional_projects_2', on_delete=models.CASCADE,
                                          null=True, blank=True, verbose_name="Дополнительный тип 2")
    additional_type_3 = models.ForeignKey(Type, related_name='additional_projects_3', on_delete=models.CASCADE,
                                          null=True, blank=True, verbose_name="Дополнительный тип 3")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Улица")
    house_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Номер дома")
    creation_year = models.CharField(max_length=4, blank=True, null=True, verbose_name="Год создания")
    design_year = models.CharField(max_length=4, blank=True, null=True, verbose_name="Год проектирования")
    project_author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Автор проекта")
    project_description = models.TextField(blank=True, null=True, verbose_name="Описание проекта")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    awards = models.TextField(blank=True, null=True, verbose_name="Награды")
    is_monitoring = models.BooleanField(default=False, verbose_name="Мониторинг")
    monitoring_parameters = models.TextField(blank=True, null=True, verbose_name="Параметры мониторинга")
    monitoring_start_year = models.CharField(max_length=4, blank=True, null=True, verbose_name="Год начала мониторинга")
    monitoring_equipment = models.CharField(max_length=255, blank=True, null=True,
                                            verbose_name="Оборудование мониторинга")
    monitoring_owner = models.CharField(max_length=255, blank=True, null=True, verbose_name="Владелец мониторинга")
    is_data_open = models.BooleanField(default=False, verbose_name="Данные открыты")
    is_ecosystem_services_measured = models.BooleanField(default=False, verbose_name="Экосистемные услуги измерены")
    ecosystem_services_measured = models.TextField(blank=True, null=True, verbose_name="Измеренные экосистемные услуги")
    ecosystem_services_desired = models.JSONField(blank=True, null=True, default=list,
                                                  verbose_name="Желаемые экосистемные услуги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


def project_photo_path(instance, filename):
    # Создание пути для фотографий проекта
    return os.path.join('photos', str(instance.project.id), filename)


class Photo(models.Model):
    project = models.ForeignKey(Project, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=project_photo_path)
    description = models.TextField(blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Фотографию"
        verbose_name_plural = "Фотографии"


class Video(models.Model):
    project = models.ForeignKey(Project, related_name='videos', on_delete=models.CASCADE)
    video = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Video for {self.project.title}'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class Link(models.Model):
    project = models.ForeignKey(Project, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Доп. материал"
        verbose_name_plural = "Доп. материалы"


class AboutPage(models.Model):
    title = models.CharField(max_length=255, default="О проекте")
    content = RichTextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "О проекте"
        verbose_name_plural = "О проекте"


class CatalogItem(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Каталог"
        verbose_name_plural = "Каталог"
