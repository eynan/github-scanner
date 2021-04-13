from django.test import TestCase

from scan.models import User, Repository
from scan.serializers import UserSerializer, RespositorySerializer
from scan.tests.utils import get_repository_struct


class UserSerializerTests(TestCase):
    def test_contains_expected_fields(self):
        user = User.objects.create(id=1, login='user', url='http://teste.com')
        serializer = UserSerializer(instance=user)

        data = serializer.data

        self.assertEqual({f.name for f in User._meta.fields}, set(data.keys()))


class RepositorySerializerTests(TestCase):
    def test_contains_expected_fields(self):
        user = User.objects.create(id=1, login='user', url='http://teste.com',)
        repository = Repository.objects.create(**get_repository_struct(id=1, user_id=1))
        serializer = RespositorySerializer(instance=repository)

        data = serializer.data

        self.assertEqual({f.attname for f in Repository._meta.fields}, set(data.keys()))
