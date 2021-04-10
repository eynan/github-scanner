from django.test import TestCase

from scan.gateways.user_gateway import get_last_user_id_created, create_users_in_lot
from scan.models import User


class GetLastUserIdCreatedTests(TestCase):
    def test_return_zero_when_not_exist_users_in_database(self):
        result = get_last_user_id_created()

        self.assertEqual(0, result)

    def test_return_bigger_user_id_in_database(self):
        bigger_id = 2
        User.objects.create(id=1, url='www.test.com', login='login')
        User.objects.create(id=bigger_id, url='www.test.com', login='login')

        result = get_last_user_id_created()

        self.assertEqual(bigger_id, result)


class CreateUsersInLotTests(TestCase):
    def test_create_many_users(self):
        user_one = {'id': 1, 'url': 'www.test.com', 'login': 'test'}
        user_two = {'id': 2, 'url': 'www.test.com', 'login': 'test'}

        create_users_in_lot([user_one, user_two])

        bd_users = User.objects.all().order_by('id')
        self.assertEqual(2, len(bd_users))
        self.assertEqual(user_one['id'], bd_users[0].id)
        self.assertEqual(user_two['id'], bd_users[1].id)
