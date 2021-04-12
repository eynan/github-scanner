import json
from unittest.mock import patch, call, AsyncMock, MagicMock

from django.test import SimpleTestCase

from scan.exceptions import GithubException
from scan.gateways.github_gateway import fetch_github_users_greater_then_the_last_user_id, fetch_login_repository, \
    parse_github_repository_to_repository
from scan.tests.utils import HttpResponseFake


class FetchGithubUsersGreaterThenTheLastUserIdTests(SimpleTestCase):
    @patch('scan.gateways.github_gateway.requests')
    def test_call_correct_endpoint(self, mock_requests):
        mock_requests.get.return_value = HttpResponseFake(status_code=200, content=json.dumps([]))
        last_user_id = 99
        fetch_github_users_greater_then_the_last_user_id(last_user_id)

        expected_parameters = {
            'accept': 'application/vnd.github.v3+json',
            'since': last_user_id,
            'per_page': 30
        }
        mock_requests.get.assert_called_once_with('https://api.github.com/users', params=expected_parameters)

    @patch('scan.gateways.github_gateway.requests')
    def test_return_list_of_user_when_request_is_correct(self, mock_requests):
        expected_users = [
            {
                'id': 1,
                'login': 'teste',
                'url': 'http://teste.com'
            },
            {
                'id': 2,
                'login': 'teste_2',
                'url': 'http://teste2.com'
            }]
        mock_requests.get.return_value = HttpResponseFake(status_code=200, content=json.dumps(expected_users))

        result = fetch_github_users_greater_then_the_last_user_id(0)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], expected_users[0]['id'])
        self.assertEqual(result[0]['login'], expected_users[0]['login'])
        self.assertEqual(result[0]['url'], expected_users[0]['url'])

    @patch('scan.gateways.github_gateway.requests')
    @patch('scan.gateways.github_gateway.time')
    @patch('scan.gateways.github_gateway.sleep')
    def test_await_a_time_to_reset_limit_requests_when_github_return_status_403(self, mock_sleep, mock_time, mock_requests):
        time_now = 200
        time_to_reset = 201
        mock_time.return_value = time_now
        mock_requests.get.side_effect = [
            HttpResponseFake(status_code=403, reason='rate limit exceeded', headers={'X-RateLimit-Reset': time_to_reset}),
            HttpResponseFake(status_code=200, content=json.dumps([])),
        ]

        fetch_github_users_greater_then_the_last_user_id(0)

        mock_sleep.assert_called_once_with(time_to_reset - time_now)

    @patch('scan.gateways.github_gateway.requests')
    @patch('scan.gateways.github_gateway.time')
    @patch('scan.gateways.github_gateway.sleep')
    def test_dont_await_a_time_to_reset_when_the_time_to_reset_has_passed(self, mock_sleep, mock_time, mock_requests):
        time_now = 200
        time_to_reset = 199
        mock_time.return_value = time_now
        mock_requests.get.side_effect = [
            HttpResponseFake(status_code=403, reason='rate limit exceeded', headers={'X-RateLimit-Reset': time_to_reset}),
            HttpResponseFake(status_code=200, content=json.dumps([])),
        ]

        fetch_github_users_greater_then_the_last_user_id(0)

        mock_sleep.assert_not_called()

    @patch('scan.gateways.github_gateway.requests')
    @patch('scan.gateways.github_gateway.time')
    @patch('scan.gateways.github_gateway.sleep')
    def test_make_the_same_request_when_time_to_reset_end(self, _, mock_time, mock_requests):
        time_now = 200
        time_to_reset = 201
        mock_time.return_value = time_now
        mock_requests.get.side_effect = [
            HttpResponseFake(status_code=403, reason='rate limit exceeded', headers={'X-RateLimit-Reset': time_to_reset}),
            HttpResponseFake(status_code=200, content=json.dumps([])),
        ]

        fetch_github_users_greater_then_the_last_user_id(0)

        expected_parameters = {
            'accept': 'application/vnd.github.v3+json',
            'since': 0,
            'per_page': 30
        }
        self.assertEqual(mock_requests.get.call_count, 2)
        self.assertEqual([call('https://api.github.com/users', params=expected_parameters)] * 2, mock_requests.get.mock_calls)

    @patch('scan.gateways.github_gateway.requests')
    def test_raise_exception_when_github_return_other_error(self, mock_requests):
        mock_requests.get.return_value = HttpResponseFake(status_code=500, reason='Bad request')

        with self.assertRaises(GithubException) as context:
            fetch_github_users_greater_then_the_last_user_id(0)

        self.assertEqual('Github api returned the status code 500, reason: Bad request, detail: last user id: 0.', str(context.exception))


class FetchLoginRepositoryAsyncTests(SimpleTestCase):
    async def test_call_correct_endpoint(self):
        client_session_mock = MagicMock()
        self._set_get_mock_response(client_session_mock, status=200, headers={}, json_data=[])

        await fetch_login_repository(client_session_mock, login='test', page=1)

        client_session_mock.get.assert_called_once_with(
            'https://api.github.com/users/test/repos',
            params={'accept': 'application/vnd.github.v3+json', 'per_page': 100, 'page': 1, 'type': 'owner'}
        )

    async def test_get_repositories_when_requests_return_status_200(self):
        client_session_mock = MagicMock()
        self._set_get_mock_response(client_session_mock, status=200, headers={}, json_data=self._get_fake_github_repository())

        response = await fetch_login_repository(client_session_mock, login='test', page=1)

        repository_expected = parse_github_repository_to_repository(self._get_fake_github_repository()[0])
        self.assertEqual(response, [repository_expected])

    async def test_get_all_pages_when_headers_return_link_for_next_pages(self):
        client_session_mock = MagicMock()
        link_next_page = '<https://api.github.com/user/134/repos?page=2&per_page=100&type=owner>; rel="next"'
        client_session_mock.get.return_value.__aenter__.side_effect = [
            MagicMock(status=200, headers={'Link': link_next_page}, json=AsyncMock(return_value=self._get_fake_github_repository(id_user=77))),
            MagicMock(status=200, headers={}, json=AsyncMock(return_value=self._get_fake_github_repository(id_user=88)))
        ]

        result = await fetch_login_repository(client_session_mock, 'test', 1)

        params_expected = {
            'accept': 'application/vnd.github.v3+json',
            'per_page': 100,
            'type': 'owner'
        }
        call_one = call('https://api.github.com/users/test/repos', params={**params_expected, **{'page': 1}})
        call_two = call('https://api.github.com/users/test/repos', params={**params_expected, **{'page': 2}})
        self.assertEqual([call_one, call_two], client_session_mock.get.call_args_list)
        self.assertEqual(77, result[0]['id'])
        self.assertEqual(88, result[1]['id'])

    @patch('scan.gateways.github_gateway.asyncio.sleep')
    @patch('scan.gateways.github_gateway.time')
    async def test_sleep_until_the_restart_github_time_ends(self, mock_time, mock_sleep):
        time_now = 200
        time_to_reset = 201
        mock_time.return_value = time_now
        mock_sleep.return_value = AsyncMock()
        client_session_mock = MagicMock()
        client_session_mock.get.return_value.__aenter__.side_effect = [
            MagicMock(status=403, headers={'X-RateLimit-Reset': time_to_reset}),
            MagicMock(status=200, headers={}, json=AsyncMock(return_value=self._get_fake_github_repository(id_user=88)))
        ]

        await fetch_login_repository(client_session_mock, 'test', 1)

        mock_sleep.assert_called_once_with(time_to_reset - time_now)

    @patch('scan.gateways.github_gateway.asyncio.sleep')
    @patch('scan.gateways.github_gateway.time')
    async def test_make_the_same_request_when_time_to_reset_end(self, mock_time, mock_sleep):
        mock_time.return_value = 200
        mock_sleep.return_value = AsyncMock()
        client_session_mock = MagicMock()
        client_session_mock.get.return_value.__aenter__.side_effect = [
            MagicMock(status=403, headers={'X-RateLimit-Reset': 201}),
            MagicMock(status=200, headers={}, json=AsyncMock(return_value=self._get_fake_github_repository(id_user=88)))
        ]

        await fetch_login_repository(client_session_mock, 'test', 1)

        expected_parameters = {'accept': 'application/vnd.github.v3+json', 'per_page': 100, 'page': 1, 'type': 'owner'}
        self.assertEqual([call('https://api.github.com/users/test/repos', params=expected_parameters)] * 2, client_session_mock.get.call_args_list)

    @patch('scan.gateways.github_gateway.asyncio.sleep')
    @patch('scan.gateways.github_gateway.time')
    async def test_dont_await_a_time_to_reset_when_the_time_to_reset_has_passed(self, mock_time, mock_sleep):
        time_now = 200
        time_to_reset = 199
        mock_time.return_value = time_now
        mock_sleep.return_value = AsyncMock()
        client_session_mock = MagicMock()
        client_session_mock.get.return_value.__aenter__.side_effect = [
            MagicMock(status=403, headers={'X-RateLimit-Reset': time_to_reset}),
            MagicMock(status=200, headers={}, json=AsyncMock(return_value=self._get_fake_github_repository(id_user=88)))
        ]

        await fetch_login_repository(client_session_mock, 'test', 1)

        mock_sleep.assert_not_called()

    async def test_raise_exception_when_github_return_other_error(self):
        client_session_mock = MagicMock()
        self._set_get_mock_response(client_session_mock, status=500, headers={}, json_data=[], reason='Bad request')

        with self.assertRaises(GithubException) as context:
            await fetch_login_repository(client_session_mock, 'test', 1)

        self.assertEqual('Github api returned the status code 500, reason: Bad request, detail: Login: test, page: 1.', str(context.exception))

    def _set_get_mock_response(self, mock_get, status, headers, json_data, reason=None):
        mock_get.get.return_value.__aenter__.return_value.status = status
        mock_get.get.return_value.__aenter__.return_value.headers = headers
        mock_get.get.return_value.__aenter__.return_value.reason = reason
        mock_get.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=json_data)

    def _get_fake_github_repository(self, id_user=99):
        return [{
            'id': id_user,
            'owner': {'id': 1},
            'description': 'Breath of the Wild is an action-adventure game set in an open world while controlling Link',
            'name': 'Breath of the Wild',
            'full_name': 'nintendo/Breath_of_the_Wild.github.io',
            'created_at': '2017-03-03T06:42:06Z',
            'updated_at': '2017-03-06T06:42:06Z',
            'pushed_at': '2017-03-03T06:42:06Z',
            'language': 'kokorik',
            'forks_count': 2,
            'stargazers_count': 3,
            'watchers_count': 4
        }]
