from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)  # HEX color code

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
    additional_types = models.ManyToManyField(Type, related_name='additional_projects', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
