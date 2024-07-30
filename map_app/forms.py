from django import forms
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
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['main_type'].queryset = Type.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['main_type'].queryset = self.instance.category.type_set.order_by('name')

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

PhotoFormSet = forms.inlineformset_factory(Project, Photo, fields=('image', 'description', 'is_main'), extra=4, can_delete=True)
VideoFormSet = forms.inlineformset_factory(Project, Video, fields=('video', 'description'), extra=1, can_delete=True)
LinkFormSet = forms.inlineformset_factory(Project, Link, fields=('url', 'description'), extra=1, can_delete=True)
