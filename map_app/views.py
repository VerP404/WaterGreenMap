import logging
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from WaterGreenMap import settings
from map_app.forms import ProjectForm, PhotoFormSet, VideoFormSet, LinkFormSet
from map_app.models import Type, Link, Video, Photo
from django.contrib import messages


def map(request):
    return render(request, 'pages/map.html')


def profile_view(request):
    return render(request, 'pages/profile.html')


def project_list_view(request):
    return render(request, 'pages/project_list.html')


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
            project.save()

            photo_formset.instance = project

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
    })


def get_types_by_category(request, category_id):
    types = Type.objects.filter(category_id=category_id)
    types_list = [{'id': type.id, 'name': type.name} for type in types]
    return JsonResponse({'types': types_list})


def get_types_by_categories(request):
    category_ids = request.GET.get('categories', '').split(',')
    types = Type.objects.filter(category_id__in=category_ids)
    types_list = [{'id': type.id, 'name': type.name} for type in types]
    return JsonResponse({'types': types_list})
