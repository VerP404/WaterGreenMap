from django.contrib import admin
from .models import CustomUser, ActivityArea, LegalDocument


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'country', 'city', 'is_staff', 'registration_date', 'auto_publish',
        'email_confirmed')
    readonly_fields = ('registration_date',)
    fields = (
        'email', 'first_name', 'last_name', 'country', 'city', 'workplace', 'phone', 'position', 'activity_area',
        'is_active', 'is_staff', 'avatar', 'registration_date', 'auto_publish', 'email_confirmed'
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'created_at')
    search_fields = ('title', 'version')
    ordering = ('-created_at',)

    class Meta:
        verbose_name = "Правовой документ"
        verbose_name_plural = "Правовые документы"


admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ActivityArea)
