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


logger = logging.getLogger('project')


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        photo_formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())
        video_formset = VideoFormSet(request.POST, queryset=Video.objects.none())
        link_formset = LinkFormSet(request.POST, queryset=Link.objects.none())

        if form.is_valid() and photo_formset.is_valid() and video_formset.is_valid() and link_formset.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.latitude = request.POST.get('latitude')
            project.longitude = request.POST.get('longitude')
            project.save()

            logger.debug(f"Project '{project.title}' saved successfully")

            # Создание папки для фотографий проекта
            project_folder = os.path.join(settings.MEDIA_ROOT, 'photos', str(project.id))
            os.makedirs(project_folder, exist_ok=True)

            # Сохранение фото
            for index, photo_form in enumerate(photo_formset):
                if photo_form.cleaned_data and 'image' in photo_form.cleaned_data:
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

                    logger.debug(f"Photo '{photo.image}' for project '{project.title}' saved successfully")

            # Сохранение видео
            for video_form in video_formset:
                if video_form.cleaned_data:
                    video = video_form.save(commit=False)
                    video.project = project
                    video.save()
                    logger.debug(f"Video '{video.video}' for project '{project.title}' saved successfully")

            # Сохранение ссылок
            for link_form in link_formset:
                if link_form.cleaned_data:
                    link = link_form.save(commit=False)
                    link.project = project
                    link.save()
                    logger.debug(f"Link '{link.url}' for project '{project.title}' saved successfully")

            messages.success(request, 'Проект успешно добавлен!')
            return redirect('project_list')
        else:
            logger.error(f"Project Form errors: {form.errors}")
            logger.error(f"Photo Formset errors: {photo_formset.errors}")
            logger.error(f"Video Formset errors: {video_formset.errors}")
            logger.error(f"Link Formset errors: {link_formset.errors}")
            messages.error(request, 'Произошла ошибка при добавлении проекта. Пожалуйста, проверьте введенные данные.')

    else:
        form = ProjectForm()
        photo_formset = PhotoFormSet(queryset=Photo.objects.none())
        video_formset = VideoFormSet(queryset=Video.objects.none())
        link_formset = LinkFormSet(queryset=Link.objects.none())

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
