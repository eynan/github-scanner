from django.test import TestCase
from django.utils import timezone

from scan.models import User, Repository

MAX_STRING_SIZE = 'a' * 191


def _create_user(**data):
    return User.objects.create(**data)


def _create_repository(**data):
    return Repository.objects.create(**data)


class UserTest(TestCase):
    def test_user_creation(self):
        data = {
            'id': 11,
            'login': 'login',
            'url': MAX_STRING_SIZE
        }

        user = _create_user(**data)

        self.assertTrue(isinstance(user, User))
        self.assertEqual(str(user), data['login'])


class RepositoryTest(TestCase):
    def test_repository_creation(self):
        user = _create_user(id=2, login='teste', url='http://teste.com')
        data = {
            'id': 11,
            'user': user,
            'description': MAX_STRING_SIZE,
            'name': 'teste',
            'full_name': MAX_STRING_SIZE,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'pushed_at': timezone.now(),
            'language': MAX_STRING_SIZE,
            'forks_count': 1,
            'stargazers_count': 2,
            'watchers_count': 3,
        }

        repository = _create_repository(**data)

        self.assertTrue(isinstance(repository, Repository))
        self.assertEqual(str(repository), data['name'])
