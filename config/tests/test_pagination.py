import json
from scan.models import User
from rest_framework.test import APITestCase


class PaginationTests(APITestCase):
    def test_pagination(self):
        user_one = User.objects.create(id=1, login='teste', url='')
        user_two = User.objects.create(id=2, login='teste_2', url='')

        response_one = self.client.get('/users?per_page=1')
        response_two = self.client.get('/users?per_page=1&page=2')

        content_one = json.loads(response_one.content)
        self.assertEqual(content_one['count'], 2)
        self.assertEqual(content_one['next'], 'http://testserver/users?page=2&per_page=1')
        self.assertIsNone(content_one['previous'])
        self.assertEqual(len(content_one['results']), 1)
        self.assertEqual(content_one['results'][0]['id'], user_one.id)
        content_two = json.loads(response_two.content)
        self.assertEqual(content_two['count'], 2)
        self.assertEqual(content_two['previous'], 'http://testserver/users?per_page=1')
        self.assertIsNone(content_two['next'])
        self.assertEqual(len(content_two['results']), 1)
        self.assertEqual(content_two['results'][0]['id'], user_two.id)
