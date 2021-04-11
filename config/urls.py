from django.urls import path

from scan.views import UserApiView, RepositoryApiView

urlpatterns = [
    path('users', UserApiView.as_view()),
    path('repositories', RepositoryApiView.as_view())
]
