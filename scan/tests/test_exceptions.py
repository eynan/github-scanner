from unittest.case import TestCase

from scan.exceptions import GithubException


class GithubExceptionTests(TestCase):
    def test_return_formatted_message(self):
        def fn():
            raise GithubException(code=500, reason='Bad request', detail='wrong login')

        with self.assertRaises(GithubException) as context:
            fn()
        self.assertEqual('Github api returned the status code 500, reason: Bad request, detail: wrong login.', str(context.exception))
