from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from scan.log import create_log_error


class LogTests(TestCase):
    @patch('scan.log.logging')
    def test_log_exception(self, logger_mock):
        mock_log_error = MagicMock()
        logger_mock.getLogger.return_value = mock_log_error
        exception = Exception('Critical damage')

        create_log_error(exception)

        mock_log_error.error.assert_called_with('Critical damage')

