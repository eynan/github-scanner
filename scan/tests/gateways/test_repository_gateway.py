from django.test import TestCase

from scan.gateways.repository_gateway import create_repositories_in_lot
from scan.models import User, Repository
from scan.tests.utils import get_repository_struct


class CreateRepositoriesInLottests(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, login='teste', url='www.tests.com')

    def test_create_many_repositories(self):
        repostitory_one = get_repository_struct(1, self.user.id)
        repostitory_two = get_repository_struct(2, self.user.id)

        create_repositories_in_lot([repostitory_one, repostitory_two])

        repositories = Repository.objects.all().order_by('id')
        self.assertEqual(2, len(repositories))
        self.assertEqual(repostitory_one['id'], repositories[0].id)
        self.assertEqual(repostitory_two['id'], repositories[1].id)
