from django.contrib import admin
from .models import CustomUser, ActivityArea, LegalDocument


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'country', 'city', 'is_staff', 'registration_date', 'auto_publish')
    readonly_fields = ('registration_date',)
    fields = (
        'email', 'first_name', 'last_name', 'country', 'city', 'workplace', 'phone', 'position', 'activity_area',
        'is_active', 'is_staff', 'avatar', 'registration_date', 'auto_publish'
    )


class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'created_at')
    search_fields = ('title', 'version')
    ordering = ('-created_at',)


admin.site.register(LegalDocument, LegalDocumentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ActivityArea)
