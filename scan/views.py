from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from scan.Filters import UserFilterSet, RepositoryFilterSet
from scan.models import User, Repository
from scan.serializers import UserSerializer, RespositorySerializer


class UserApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilterSet
    ordering_fields = '__all__'
    ordering = ['id']


class RepositoryApiView(ListAPIView):
    queryset = Repository.objects.all()
    serializer_class = RespositorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_class = RepositoryFilterSet
    ordering_fields = [
        'id', 'user_id', 'description', 'name',
        'full_name', 'created_at', 'updated_at',
        'pushed_at', 'language', 'forks_count',
        'stargazers_count', 'watchers_count'
    ]
    ordering = ['id']
