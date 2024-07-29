from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from map_app.views import map, profile_view, project_list_view, add_project, get_types_by_category, \
    get_types_by_categories
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/', include('accounts.urls')),
                  path('', map, name='map'),
                  path('profile/', profile_view, name='profile'),
                  path('project_list/', project_list_view, name='project_list'),
                  path('add_project/', add_project, name='add_project'),
                  path('get_types_by_category/<int:category_id>/', get_types_by_category,
                       name='get_types_by_category'),
                  path('get_types_by_categories/', get_types_by_categories, name='get_types_by_categories'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
