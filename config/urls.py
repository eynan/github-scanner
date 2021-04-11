from django.contrib import admin
from django.urls import path

from scan.views import UserApiView, RepositoryApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', UserApiView.as_view()),
    path('repositories', RepositoryApiView.as_view())
]
