# projects
from django.urls import path, register_converter
from . import views

app_name = 'projects'


class FloatConverter:
    regex = '[0-9]+(?:\.[0-9]+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


register_converter(FloatConverter, 'float')
urlpatterns = [
    path('add/<float:lat>/<float:lng>/', views.add_project, name='add_project'),
]
