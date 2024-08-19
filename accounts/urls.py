from django.urls import path
from .views import SignUpView, SignInView, SignOutView, ProfileUpdateView, DocumentDownloadView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('documents/download/<slug:slug>/', DocumentDownloadView.as_view(), name='document_download'),
]
