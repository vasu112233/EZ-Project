from django.urls import path, include
from ez_backend_test.views import signup, login_view, ActivateAccountView, FileListView, FileUploadView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('api/files/', FileListView.as_view(), name='file-list'),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
]
