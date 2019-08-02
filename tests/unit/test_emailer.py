import json
import unittest
from unittest import mock
from pathlib import Path
from auto_emailer import Emailer
from auto_emailer.config import credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_ENVIR_JSON_FILE = str(DATA_DIR / 'mock_envir_credentials.json')
MOCK_USER_JSON_FILE = str(DATA_DIR / 'mock_user_credentials.json')


def _get_mock_credentials(file):
    with open(file, 'r') as creds:
        return json.load(creds)


class TestEmailer(unittest.TestCase):

    # @staticmethod
    # def _make_credentials(data):
    #     """
    #     """
    #     return mock.Mock(credentials.Credentials(**data))

    @staticmethod
    def _make_credentials(data):
        """
        """
        return credentials.Credentials(**data)

    def test_emailer_config_error(self):
        """
        """
        with self.assertRaises(ValueError):
            Emailer(config="My data")

    def test_emailer_none_error(self):
        """
        """
        with self.assertRaises(ValueError):
            Emailer()

    @mock.patch('auto_emailer.emailer.default_credentials')
    def test_emailer_defaults(self, mock_default):
        """
        """
        data = _get_mock_credentials(MOCK_USER_JSON_FILE)
        mock_default.return_value = self._make_credentials(data)
        test_emailer = Emailer()
        self.assertIsInstance(test_emailer, Emailer)
        self.assertFalse(test_emailer.logged_in)
        mock_default.assert_called_once_with()

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_logged_in(self, mock_smtplib):
        """
        """
        data = _get_mock_credentials(MOCK_USER_JSON_FILE)
        creds = self._make_credentials(data)
        test_emailer = Emailer(config=creds, delay_login=False)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.logged_in)
        self.assertEqual(mock_smtplib.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_logout(self, mock_smtplib):
        """
        """
        # the mock_smtplib is a pointer to
        # the mocked class not to the mocked instance of SMTP
        instance = mock_smtplib.return_value
        print(instance)
        data = _get_mock_credentials(MOCK_USER_JSON_FILE)
        creds = self._make_credentials(data)
        test_emailer = Emailer(config=creds, delay_login=False)
        print(instance)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.logged_in)
        test_emailer._logout()
        self.assertFalse(test_emailer.logged_in)
        print(instance.method_calls)
        instance.quit.assert_called_once_with()

    # @mock.patch('auto_emailer.emailer.smtplib.STMP')
    # def test_emailer_login(self, mock_smtplib):
    #     """
    #     """
    #     data = _get_mock_credentials(MOCK_USER_JSON_FILE)
    #     creds = self._make_credentials(data)
    #     mock_smtplib.return_value.SMTP.return_value.quit.return_value = True
    #     test_emailer = Emailer(config=creds, delay_login=False)
    #
    #     self.assertIsInstance(test_emailer, Emailer)
    #     self.assertTrue(test_emailer.logged_in)
    #     test_emailer._logout()
    #
    #     self.assertFalse(test_emailer.logged_in)
    #     mock_smtplib.SMTP.quit.assert_called_once_with()
    #     # mock_smtplib.



if __name__ == '__main__':
    unittest.main()
