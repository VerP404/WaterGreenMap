from django.contrib import admin
from .models import Category, Type, Project
from django.utils.html import format_html

class ColorAdminMixin:
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.color
        )
    color_display.short_description = 'Цвет'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ColorAdminMixin):
    list_display = ('name', 'description', 'color_display', 'color')
    list_editable = ('color',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin, ColorAdminMixin):
    list_display = ('name', 'description', 'category', 'color_display', 'color')
    list_editable = ('color',)
    list_filter = ('category',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_type', 'user', 'is_published', 'created_at')
    list_filter = ('main_type', 'user', 'is_published')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('is_published',)
