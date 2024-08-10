import os
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)  # HEX color code
    icon = models.CharField(max_length=50, default="archive")  # Имя иконки

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)  # HEX color code
    category = models.ForeignKey(Category, related_name='types', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    main_type = models.ForeignKey(Type, related_name='main_projects', on_delete=models.CASCADE)
    additional_type_1 = models.ForeignKey(Type, related_name='additional_projects_1', on_delete=models.CASCADE,
                                          null=True, blank=True)
    additional_type_2 = models.ForeignKey(Type, related_name='additional_projects_2', on_delete=models.CASCADE,
                                          null=True, blank=True)
    additional_type_3 = models.ForeignKey(Type, related_name='additional_projects_3', on_delete=models.CASCADE,
                                          null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    creation_year = models.CharField(max_length=4, blank=True, null=True)
    design_year = models.CharField(max_length=4, blank=True, null=True)
    project_author = models.CharField(max_length=255, blank=True, null=True)
    project_description = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    is_monitoring = models.BooleanField(default=False)
    monitoring_parameters = models.TextField(blank=True, null=True)
    monitoring_start_year = models.CharField(max_length=4, blank=True, null=True)
    monitoring_equipment = models.CharField(max_length=255, blank=True, null=True)
    monitoring_owner = models.CharField(max_length=255, blank=True, null=True)
    is_data_open = models.BooleanField(default=False)
    is_ecosystem_services_measured = models.BooleanField(default=False)
    ecosystem_services_measured = models.TextField(blank=True, null=True)
    ecosystem_services_desired = models.JSONField(blank=True, null=True, default=list)

    def __str__(self):
        return self.title


def project_photo_path(instance, filename):
    # Создание пути для фотографий проекта
    return os.path.join('photos', str(instance.project.id), filename)


class Photo(models.Model):
    project = models.ForeignKey(Project, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=project_photo_path)
    description = models.TextField(blank=True)
    is_main = models.BooleanField(default=False)


class Video(models.Model):
    project = models.ForeignKey(Project, related_name='videos', on_delete=models.CASCADE)
    video = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Video for {self.project.title}'


class Link(models.Model):
    project = models.ForeignKey(Project, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.url


class AboutPage(models.Model):
    title = models.CharField(max_length=255, default="О проекте")
    content = RichTextField()

    def __str__(self):
        return self.title
