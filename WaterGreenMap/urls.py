from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from map_app.views import map, profile_view, project_list_view
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('accounts.urls')),
                  path('projects/', include('projects.urls')),
                  path('', map, name='map'),
                  path('profile/', profile_view, name='profile'),
                  path('project_list/', project_list_view, name='project_list'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
