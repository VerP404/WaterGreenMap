from django.contrib import admin
from .models import Category, Type, Project, Photo, Video, Link, AboutPage, CatalogItem
from django.utils.html import format_html


class ColorAdminMixin:
    class Media:
        js = ('admin/js/color_preview.js',)  # Путь к вашему JS файлу

    def color_display(self, obj):
        return format_html(
            '<div class="color-preview" style="width: 20px; height: 20px; background-color: {}; border: 1px solid #000;"></div>',
            obj.color
        )

    color_display.short_description = 'Цвет'


class TypeInline(admin.TabularInline):
    model = Type
    extra = 1


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ColorAdminMixin):
    list_display = ('name', 'description', 'color_display', 'color')
    list_editable = ('color',)
    inlines = [TypeInline]


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Preview'


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class LinkInline(admin.TabularInline):
    model = Link
    extra = 1


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('project', 'image_tag', 'description', 'is_main')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "-"

    image_tag.short_description = 'Preview'


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('project', 'video', 'description')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('project', 'url', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'main_type', 'user', 'is_published', 'created_at', 'image_preview', 'video_links', 'additional_links')
    list_filter = ('main_type', 'user', 'is_published', 'country', 'city', 'creation_year')
    search_fields = ('title', 'description', 'user__email')
    list_editable = ('is_published',)
    inlines = [PhotoInline, VideoInline, LinkInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(ProjectAdmin, self).get_inline_instances(request, obj)

    def image_preview(self, obj):
        photos = obj.photos.all()
        if photos.exists():
            photo = photos.first()
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', photo.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"

    def video_links(self, obj):
        videos = obj.videos.all()
        links = [format_html('<a href="{}" target="_blank">{}</a>', video.video, video.description) for video in videos]
        return format_html("<br>".join(links))

    video_links.short_description = "Ссылки на видео"

    def additional_links(self, obj):
        links = obj.links.all()
        additional_links = [format_html('<a href="{}" target="_blank">{}</a>', link.url, link.description) for link in
                            links]
        return format_html("<br>".join(additional_links))

    additional_links.short_description = "Дополнительные ссылки"
