from datetime import datetime
from unittest.case import TestCase

from scan.gateways.github_gateway import parse_github_user_to_user, parse_github_repository_to_repository, DATE_FORMAT_GITHUB


class ParseGithubUserToUserTests(TestCase):
    def test_parse_github_user_to_user(self):
        github_return = {
            'id': 2,
            'login': 'test',
            'url': 'http://test.com',
            'other_field': 'aaaaaa'
        }

        result = parse_github_user_to_user(github_return)

        del github_return['other_field']
        self.assertEqual(github_return, result)


class ParseGithubRepositoryToRepositoryTests(TestCase):
    def test_parse_github_repository_to_repository(self):
        github_repository = {
            'id': 99,
            'owner': {'id': 9},
            'description': 'blablabla',
            'name': 'test',
            'full_name': 'PLUSS ULTRAA',
            'created_at': '2007-10-21T05:24:19Z',
            'updated_at': '2007-10-22T05:24:19Z',
            'pushed_at': '2007-10-23T05:24:19Z',
            'language': 'rust',
            'forks_count': 2,
            'stargazers_count': 3,
            'watchers_count': 4,
            'other_field': 'Its me mario!'
        }

        result = parse_github_repository_to_repository(github_repository)

        repository_expected = {
            'id': 99,
            'user_id': 9,
            'description': 'blablabla',
            'name': 'test',
            'full_name': 'PLUSS ULTRAA',
            'created_at': datetime.strptime('2007-10-21T05:24:19Z', DATE_FORMAT_GITHUB),
            'updated_at': datetime.strptime('2007-10-22T05:24:19Z', DATE_FORMAT_GITHUB),
            'pushed_at': datetime.strptime('2007-10-23T05:24:19Z', DATE_FORMAT_GITHUB),
            'language': github_repository['language'],
            'forks_count': github_repository['forks_count'],
            'stargazers_count': github_repository['stargazers_count'],
            'watchers_count': github_repository['watchers_count']
        }
        self.assertEqual(repository_expected, result)
