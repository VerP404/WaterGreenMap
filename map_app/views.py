from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from map_app.forms import ProjectForm, PhotoFormSet, VideoFormSet, LinkFormSet
from map_app.models import Type, Link, Video, Photo


def map(request):
    return render(request, 'pages/map.html')


def profile_view(request):
    return render(request, 'pages/profile.html')


def project_list_view(request):
    return render(request, 'pages/project_list.html')

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        photo_formset = PhotoFormSet(request.POST, request.FILES, queryset=Photo.objects.none())
        video_formset = VideoFormSet(request.POST, queryset=Video.objects.none())
        link_formset = LinkFormSet(request.POST, queryset=Link.objects.none())

        if form.is_valid() and photo_formset.is_valid() and video_formset.is_valid() and link_formset.is_valid():
            project = form.save()
            for index, photo_form in enumerate(photo_formset):
                photo = photo_form.save(commit=False)
                photo.project = project
                if index == 0:
                    photo.is_main = True
                photo.save()
            for video_form in video_formset:
                video = video_form.save(commit=False)
                video.project = project
                video.save()
            for link_form in link_formset:
                link = link_form.save(commit=False)
                link.project = project
                link.save()
            return redirect('project_list')
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
