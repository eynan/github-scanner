from django.test import TestCase

from scan.Filters import UserFilterSet, RepositoryFilterSet
from scan.models import User, Repository


class UserFilterSetTests(TestCase):
    def test_create_filters_expected(self):
        filters = UserFilterSet({}, queryset=User.objects.all())

        expected_filters = {'id', 'id__gt', 'id__gte', 'id__lt', 'id__lte', 'id__lte', 'login'}
        self.assertEqual(set(filters.base_filters.keys()), expected_filters)


class RepositoryFilterSetTests(TestCase):
    def test_create_filters_expected(self):
        filters = RepositoryFilterSet({}, queryset=Repository.objects.all())

        expected_filters = {
            'created_at', 'created_at__gt', 'created_at__gte', 'created_at__lt', 'created_at__lte', 'forks_count', 'forks_count__gt',
            'forks_count__gte', 'forks_count__lt', 'forks_count__lte', 'id', 'id__gt', 'id__gte', 'id__lt', 'id__lte', 'language',
            'name', 'pushed_at', 'pushed_at__gt', 'pushed_at__gte', 'pushed_at__lt', 'pushed_at__lte', 'stargazers_count',
            'stargazers_count__gt', 'stargazers_count__gte', 'stargazers_count__lt', 'stargazers_count__lte', 'updated_at',
            'updated_at__gt', 'updated_at__gte', 'updated_at__lt', 'updated_at__lte', 'user', 'user__gt', 'user__gte',
            'user__lt', 'user__lte', 'watchers_count', 'watchers_count__gt', 'watchers_count__gte', 'watchers_count__lt',
            'watchers_count__lte'
        }
        self.assertEqual(set(filters.base_filters.keys()), expected_filters)
