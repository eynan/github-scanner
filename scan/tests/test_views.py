import json
from http import HTTPStatus

from rest_framework.test import APITestCase

from scan.models import User, Repository
from scan.tests.utils import get_repository_struct


class UserApiViewTests(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create(id=1, login='test', url='http://teste.com')
        self.base_url = '/users'

    def test_return_users_data(self):
        response = self.client.get(self.base_url)

        results = json.loads(response.content)['results']
        user_returned = results[0]
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(user_returned['id'], self.user_one.id)
        self.assertEqual(user_returned['login'], self.user_one.login)
        self.assertEqual(user_returned['url'], self.user_one.url)

    def test_ordering_fields(self):
        user_two = User.objects.create(id=2, login='test', url='http://teste.com')

        response = self.client.get(f'{self.base_url}?order_by=-id')

        results = json.loads(response.content)['results']
        self.assertEqual(results[0]['id'], user_two.id)
        self.assertEqual(results[1]['id'], self.user_one.id)

    def test_filter_fields(self):
        User.objects.create(id=2, login='test', url='http://teste.com')

        response = self.client.get(f'{self.base_url}?id=1')

        results = json.loads(response.content)['results']
        self.assertEqual(results[0]['id'], self.user_one.id)
        self.assertEqual(len(results), 1)


class RepositoryApiViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, login='test', url='http://teste.com')
        self.repository_one = Repository.objects.create(**get_repository_struct(self.user.id, 1))
        self.base_url = '/repositories'

    def test_return_repository_data(self):
        response = self.client.get(self.base_url)

        results = json.loads(response.content)['results']
        user_returned = results[0]
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(user_returned['id'], self.repository_one.id)
        self.assertEqual(user_returned['user_id'], self.user.id)
        self.assertEqual(user_returned['name'], self.repository_one.name)
        self.assertEqual(user_returned['full_name'], self.repository_one.full_name)
        self.assertEqual(user_returned['created_at'], self.repository_one.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(user_returned['updated_at'], self.repository_one.updated_at.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(user_returned['pushed_at'], self.repository_one.pushed_at.strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(user_returned['language'], self.repository_one.language)
        self.assertEqual(user_returned['forks_count'], self.repository_one.forks_count)
        self.assertEqual(user_returned['stargazers_count'], self.repository_one.stargazers_count)
        self.assertEqual(user_returned['watchers_count'], self.repository_one.watchers_count)

    def test_ordering_fields(self):
        repository_two = Repository.objects.create(**get_repository_struct(2, self.user.id))

        response = self.client.get(f'{self.base_url}?order_by=-id')

        results = json.loads(response.content)['results']
        self.assertEqual(results[0]['id'], repository_two.id)
        self.assertEqual(results[1]['id'], self.repository_one.id)

    def test_filter_fields(self):
        Repository.objects.create(**get_repository_struct(2, self.user.id))

        response = self.client.get(f'{self.base_url}?id=1')

        results = json.loads(response.content)['results']
        self.assertEqual(results[0]['id'], self.repository_one.id)
        self.assertEqual(len(results), 1)
