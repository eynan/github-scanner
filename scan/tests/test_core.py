from django.utils import timezone
from unittest.mock import patch

from django.test import TestCase, SimpleTestCase

from scan.core import screap_users_and_repositories_data_from_github, screap_repositories_date_from_users_logins_async
from scan.exceptions import GithubException
from scan.models import User, Repository


class ScreapDataFromGithubTests(TestCase):
    @patch('scan.core.fetch_login_repository')
    @patch('scan.core.fetch_github_users_greater_then_the_last_user_id')
    def test_create_users_returned_from_github(self, mock_fetch_users, mock_fetch_repositories):
        user_id = 55
        user_two_id = 66
        mock_fetch_users.return_value = [_get_user_struct(user_id), _get_user_struct(user_two_id)]
        mock_fetch_repositories.return_value = []

        screap_users_and_repositories_data_from_github()

        users = list(User.objects.all().order_by('id'))
        self.assertEqual(2, len(users))
        self.assertEqual(user_id, users[0].id)
        self.assertEqual(user_two_id, users[1].id)

    @patch('scan.core.fetch_login_repository')
    @patch('scan.core.fetch_github_users_greater_then_the_last_user_id')
    def test_create_repositories_returned_from_github(self, mock_fetch_users, mock_fetch_repositories):
        user_one_id = 44
        user_two_id = 55
        repository_user_one_id = 444
        repository_user_two_id = 555
        mock_fetch_users.return_value = [_get_user_struct(user_one_id), _get_user_struct(user_two_id)]
        mock_fetch_repositories.side_effect = [
            [_get_repository_struct(repository_user_one_id, user_one_id)],
            [_get_repository_struct(repository_user_two_id, user_two_id)]
        ]

        screap_users_and_repositories_data_from_github()

        repositories_user_one = list(Repository.objects.filter(user_id=user_one_id))
        self.assertEqual(1, len(repositories_user_one))
        self.assertEqual(repository_user_one_id, repositories_user_one[0].id)
        repositories_user_two = list(Repository.objects.filter(user_id=user_two_id))
        self.assertEqual(1, len(repositories_user_two))
        self.assertEqual(repository_user_two_id, repositories_user_two[0].id)


class ScreapRepositoriesDateFromUsersLoginsAsyncTests(SimpleTestCase):
    @patch('scan.core.fetch_login_repository')
    async def test_return_all_data_returned_from_logins(self, mock_request):
        logins = ['test_1', 'test_2']
        expected_list = [[_get_repository_struct(1, 11)], [_get_repository_struct(2, 22)]]
        mock_request.side_effect = expected_list

        result = await screap_repositories_date_from_users_logins_async(logins)

        self.assertEqual(expected_list, result)

    @patch('scan.core.fetch_login_repository')
    async def test_return_exception_raised_in_fetch_login_repository(self, mock_request):
        mock_request.side_effect = GithubException(500, 'Bad request')

        result = await screap_repositories_date_from_users_logins_async(['login'])

        self.assertIsInstance(result[0], GithubException)


def _get_user_struct(id):
    return {
        'id': id,
        'login': 'test',
        'url': 'http://test.com'
    }


def _get_repository_struct(id, user_id):
    return {
        'id': id,
        'user_id': user_id,
        'description': 'test',
        'name': 'test',
        'full_name': 'test',
        'created_at': timezone.now(),
        'updated_at': timezone.now(),
        'pushed_at': timezone.now(),
        'language': 'test',
        'forks_count': 2,
        'stargazers_count': 2,
        'watchers_count': 2
    }