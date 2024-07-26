from django.shortcuts import render


def map(request):
    return render(request, 'map.html')


def profile_view(request):
    return render(request, 'pages/profile.html')


def project_list_view(request):
    return render(request, 'pages/project_list.html')
