from django import forms
from django.forms import modelformset_factory
from .models import Project, Photo, Video, Link, Category, Type

class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label="Категория")
    main_type = forms.ModelChoiceField(queryset=Type.objects.none(), required=True, label="Основной тип")
    additional_category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Дополнительная категория")
    additional_type = forms.ModelChoiceField(queryset=Type.objects.none(), required=False, label="Дополнительный тип")

    class Meta:
        model = Project
        fields = ['title', 'description', 'latitude', 'longitude', 'category', 'main_type', 'additional_category', 'additional_type']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

PhotoFormSet = modelformset_factory(Photo, fields=('image', 'description', 'is_main'), extra=1)
VideoFormSet = modelformset_factory(Video, fields=('video', 'description'), extra=1)
LinkFormSet = modelformset_factory(Link, fields=('url', 'description'), extra=1)