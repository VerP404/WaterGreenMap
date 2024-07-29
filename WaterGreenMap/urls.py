from django.contrib import admin
from django.urls import path, include

from map_app.views import map, profile_view, project_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', map, name='map'),
    path('profile/', profile_view, name='profile'),
    path('project_list/', project_list_view, name='project_list'),

]
