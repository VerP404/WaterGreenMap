from django import forms
from .models import Project, Photo, Video, Link, Category, Type


class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label="Категория")
    main_type = forms.ModelChoiceField(queryset=Type.objects.none(), required=True, label="Основной тип")
    additional_category_1 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                                   label="Дополнительная категория 1")
    additional_type_1 = forms.ModelChoiceField(queryset=Type.objects.none(), required=False,
                                               label="Дополнительный тип 1")
    additional_category_2 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                                   label="Дополнительная категория 2")
    additional_type_2 = forms.ModelChoiceField(queryset=Type.objects.none(), required=False,
                                               label="Дополнительный тип 2")
    additional_category_3 = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                                   label="Дополнительная категория 3")
    additional_type_3 = forms.ModelChoiceField(queryset=Type.objects.none(), required=False,
                                               label="Дополнительный тип 3")

    is_monitoring = forms.BooleanField(required=False, label="Ведется ли мониторинг")
    is_data_open = forms.BooleanField(required=False, label="Открыты ли данные?")
    is_ecosystem_services_measured = forms.BooleanField(required=False, label="Измерялись ли экосистемные услуги")
    ecosystem_services_desired = forms.MultipleChoiceField(
        choices=[(str(i), f"Услуга {i}") for i in range(1, 31)],  # Подставьте реальные идентификаторы и названия услуг
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Экосистемные услуги"
    )

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'latitude', 'longitude', 'category', 'main_type',
            'additional_category_1', 'additional_type_1',
            'additional_category_2', 'additional_type_2',
            'additional_category_3', 'additional_type_3',
            'country', 'city', 'creation_year', 'design_year',
            'project_author', 'project_description', 'additional_info',
            'is_monitoring', 'monitoring_parameters', 'monitoring_start_year',
            'monitoring_equipment', 'monitoring_owner', 'is_data_open',
            'is_ecosystem_services_measured', 'ecosystem_services_measured',
            'ecosystem_services_desired'
        ]

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['main_type'].queryset = Type.objects.none()
        self.fields['additional_type_1'].queryset = Type.objects.none()
        self.fields['additional_type_2'].queryset = Type.objects.none()
        self.fields['additional_type_3'].queryset = Type.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['main_type'].queryset = Type.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass

        for i in range(1, 4):
            category_field = f'additional_category_{i}'
            type_field = f'additional_type_{i}'
            if category_field in self.data:
                try:
                    category_id = int(self.data.get(category_field))
                    self.fields[type_field].queryset = Type.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                related_category = getattr(self.instance, f'additional_category_{i}', None)
                if related_category:
                    self.fields[type_field].queryset = Type.objects.filter(category=related_category).order_by('name')

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


PhotoFormSet = forms.inlineformset_factory(Project, Photo, fields=('image', 'description', 'is_main'), extra=4,
                                           can_delete=True)
VideoFormSet = forms.inlineformset_factory(Project, Video, fields=('video', 'description'), extra=1, can_delete=True)
LinkFormSet = forms.inlineformset_factory(Project, Link, fields=('url', 'description'), extra=1, can_delete=True)
