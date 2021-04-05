from unittest.case import TestCase

from scan.exceptions import GithubException


class GithubExceptionTests(TestCase):
    def test_return_formatted_message(self):
        def fn():
            raise GithubException(500, 'Bad request')

        with self.assertRaises(GithubException) as context:
            fn()
        self.assertEqual('Github api returned the status code 500, reason: Bad request.', str(context.exception))
