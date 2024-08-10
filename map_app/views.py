import json
import logging
import os

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from WaterGreenMap import settings
from map_app.forms import ProjectForm, PhotoFormSet, VideoFormSet, LinkFormSet
from map_app.models import Type, Link, Video, Photo, Project, Category, AboutPage
from django.contrib import messages


def map(request):
    categories = Category.objects.all().prefetch_related('types')
    types = Type.objects.all()

    filtered_projects = Project.objects.filter(is_published=True).select_related('main_type', 'main_type__category')

    category_ids = request.GET.get('categories', '').split(',')
    type_ids = request.GET.get('types', '').split(',')

    if category_ids != [''] and category_ids[0]:
        filtered_projects = filtered_projects.filter(main_type__category_id__in=category_ids)

    if type_ids != [''] and type_ids[0]:
        filtered_projects = filtered_projects.filter(main_type_id__in=type_ids)

    projects_data = json.dumps(
        list(filtered_projects.values(
            'id', 'title', 'description', 'latitude', 'longitude',
            'main_type__color', 'main_type__category__color'
        )),
        cls=DjangoJSONEncoder
    )

    return render(request, 'pages/map.html', {
        'projects_data': projects_data,
        'categories': categories,
        'types': types
    })


def update_map(request):
    category_ids = request.GET.get('categories', '').split(',')
    type_ids = request.GET.get('types', '').split(',')

    filtered_projects = Project.objects.filter(is_published=True).select_related('main_type', 'main_type__category')

    if category_ids != [''] and category_ids[0]:
        filtered_projects = filtered_projects.filter(main_type__category_id__in=category_ids)

    if type_ids != [''] and type_ids[0]:
        filtered_projects = filtered_projects.filter(main_type_id__in=type_ids)

    projects_data = list(filtered_projects.values(
        'title', 'description', 'latitude', 'longitude',
        'main_type__color', 'main_type__category__color'
    ))

    return JsonResponse(projects_data, safe=False)


@login_required
def profile_view(request):
    user_projects = Project.objects.filter(user=request.user, is_published=True).select_related(
        'main_type').prefetch_related('photos')
    return render(request, 'pages/profile.html', {'projects': user_projects})


def project_list_view(request):
    category_id = request.GET.get('categories', '')
    type_id = request.GET.get('types', '')

    projects = Project.objects.filter(is_published=True).select_related('main_type', 'user').prefetch_related('photos')

    if category_id:
        projects = projects.filter(main_type__category_id=category_id)

    if type_id:
        projects = projects.filter(main_type_id=type_id)

    # Сортировка по новизне
    projects = projects.order_by('-created_at')

    categories = Category.objects.all()

    context = {
        'projects': projects,
        'categories': categories,
        'selected_category': Category.objects.get(id=category_id) if category_id else None,
        'selected_type': Type.objects.get(id=type_id) if type_id else None,
        'selected_category_id': category_id,
        'selected_type_id': type_id,
    }

    return render(request, 'pages/project_list.html', context)


# Настройка логгера
logger = logging.getLogger(__name__)


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        photo_formset = PhotoFormSet(request.POST, request.FILES, instance=form.instance)
        video_formset = VideoFormSet(request.POST, request.FILES, instance=form.instance)
        link_formset = LinkFormSet(request.POST, request.FILES, instance=form.instance)

        if form.is_valid() and photo_formset.is_valid() and video_formset.is_valid() and link_formset.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.latitude = request.POST.get('latitude')
            project.longitude = request.POST.get('longitude')

            # Проверяем, включена ли авто-публикация для пользователя
            project.is_published = request.user.auto_publish

            # Сохранение экосистемных услуг
            ecosystem_services_desired = request.POST.getlist('ecosystem_services_desired')
            project.ecosystem_services_desired = json.dumps(ecosystem_services_desired)

            project.save()

            # Сохранение дополнительных типов
            project.additional_type_1 = form.cleaned_data['additional_type_1']
            project.additional_type_2 = form.cleaned_data['additional_type_2']
            project.additional_type_3 = form.cleaned_data['additional_type_3']

            project.save()

            # Сохранение фото, видео и ссылок
            photo_formset.instance = project
            photo_formset.save()

            video_formset.instance = project
            video_formset.save()

            link_formset.instance = project
            link_formset.save()

            # Создание папки для фотографий проекта
            project_folder = os.path.join(settings.MEDIA_ROOT, 'photos', str(project.id))
            os.makedirs(project_folder, exist_ok=True)

            # Сохранение фото и переименование
            for index, photo_form in enumerate(photo_formset):
                if photo_form.cleaned_data.get('image'):
                    photo = photo_form.save(commit=False)
                    photo.project = project
                    if index == 0:
                        photo.is_main = True

                    # Переименование и сохранение файла
                    original_file = photo_form.cleaned_data['image']
                    filename = f"{index + 1}{os.path.splitext(original_file.name)[1]}"
                    file_path = os.path.join(project_folder, filename)
                    with open(file_path, 'wb+') as destination:
                        for chunk in original_file.chunks():
                            destination.write(chunk)

                    photo.image = os.path.join('photos', str(project.id), filename)
                    photo.save()

            messages.success(request, 'Проект успешно добавлен!')
            return redirect('project_list')
        else:
            messages.error(request, 'Произошла ошибка при добавлении проекта. Пожалуйста, проверьте введенные данные.')

    else:
        form = ProjectForm()
        photo_formset = PhotoFormSet(instance=form.instance)
        video_formset = VideoFormSet(instance=form.instance)
        link_formset = LinkFormSet(instance=form.instance)

    return render(request, 'pages/add_project.html', {
        'form': form,
        'photo_formset': photo_formset,
        'video_formset': video_formset,
        'link_formset': link_formset,
        'range_1_to_4': range(1, 4),  # Передаем диапазон в контекст для шаблона
    })


def get_types_by_category(request, category_id):
    types = Type.objects.filter(category_id=category_id).order_by('name')
    types_list = [{'id': type.id, 'name': type.name} for type in types]
    return JsonResponse({'types': types_list})


def get_types_by_categories(request):
    category_ids = request.GET.get('categories', '').split(',')
    types = Type.objects.filter(category_id__in=category_ids)
    types_list = [{'id': type.id, 'name': type.name} for type in types]
    return JsonResponse({'types': types_list})


def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Собираем все типы в один список, исключая дубликаты
    all_types = [project.main_type]
    if project.additional_type_1 and project.additional_type_1 not in all_types:
        all_types.append(project.additional_type_1)
    if project.additional_type_2 and project.additional_type_2 not in all_types:
        all_types.append(project.additional_type_2)
    if project.additional_type_3 and project.additional_type_3 not in all_types:
        all_types.append(project.additional_type_3)

    user_projects_count = Project.objects.filter(user=project.user, is_published=True).count()

    return render(request, 'pages/project_detail.html', {
        'project': project,
        'unique_types': all_types,  # Передаем уникальные типы в шаблон
        'user_projects_count': user_projects_count
    })



def about_view(request):
    about_page = AboutPage.objects.first()
    return render(request, 'pages/about.html', {'about_page': about_page})
