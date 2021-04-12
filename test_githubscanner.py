from unittest.case import TestCase
from unittest.mock import patch

import githubscanner


class TestGithubscanner(TestCase):
    @patch('githubscanner.screap_users_and_repositories_data_from_github')
    def test_run_core_function(self, mock_core):
        githubscanner.main()

        self.assertEqual(mock_core.call_count, 1)
