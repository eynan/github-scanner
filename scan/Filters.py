import django_filters

from scan.models import User, Repository

NUMBER_AND_DATE_FILTERS = ['exact', 'gt', 'lt', 'gte', 'lte']
STRING_FILTERS = ['exact']


class UserFilterSet(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': NUMBER_AND_DATE_FILTERS,
            'login': STRING_FILTERS,
        }


class RepositoryFilterSet(django_filters.FilterSet):
    class Meta:
        model = Repository
        fields = {
            'id': NUMBER_AND_DATE_FILTERS,
            'user': NUMBER_AND_DATE_FILTERS,
            'name': STRING_FILTERS,
            'created_at': NUMBER_AND_DATE_FILTERS,
            'updated_at': NUMBER_AND_DATE_FILTERS,
            'pushed_at': NUMBER_AND_DATE_FILTERS,
            'language': STRING_FILTERS,
            'forks_count': NUMBER_AND_DATE_FILTERS,
            'stargazers_count': NUMBER_AND_DATE_FILTERS,
            'watchers_count': NUMBER_AND_DATE_FILTERS
        }