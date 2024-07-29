from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm


def profile_view(request):
    return render(request, 'projects/profile.html')


def project_list_view(request):
    return render(request, 'projects/project_list.html')

@login_required
def profile_view(request):
    return render(request, 'projects/profile.html')
@login_required
def add_project(request, lat, lng):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.latitude = lat
            project.longitude = lng
            project.user = request.user
            project.save()
            form.save_m2m()
            return redirect('map')  # Redirect to the map after saving
    else:
        form = ProjectForm()
    return render(request, 'projects/add_project.html', {'form': form})


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})
