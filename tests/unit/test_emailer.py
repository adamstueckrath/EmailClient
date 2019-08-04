import json
import unittest
import smtplib
from unittest import mock
from pathlib import Path
from auto_emailer import Emailer
from auto_emailer.config import credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_USER_JSON_FILE = DATA_DIR / 'mock_user_credentials.json'


def _get_mock_credentials(file):
    with file.open() as creds:
        return json.load(creds)


class TestEmailer(unittest.TestCase):

    @staticmethod
    def _make_credentials():
        """
        Used for creating credentials.Credentials
        instance for test cases.
        """
        creds = _get_mock_credentials(MOCK_USER_JSON_FILE)
        return credentials.Credentials(**creds)

    def test_emailer_config_error(self):
        """
        Test initialization of Emailer with unknown config
        argument data type raises ValueError.
        """
        with self.assertRaises(ValueError):
            Emailer(config="My data")

    @mock.patch('auto_emailer.emailer.default_credentials')
    def test_emailer_none_error(self, mock_default):
        """
        Test initialization of Emailer raises ValueError if
        arguments are None and call to default.default_credentials()
        returns None.
        """
        mock_default.side_effect = ValueError
        with self.assertRaises(ValueError):
            Emailer()

    @mock.patch('auto_emailer.emailer.default_credentials')
    def test_emailer_defaults(self, mock_default):
        """
        Test initialization of Emailer() with default.default_credentials
        and validate smtplib is not called to login since delay_login argument
        is not passed.
        """
        mock_default.return_value = self._make_credentials()
        test_emailer = Emailer()
        self.assertIsInstance(test_emailer, Emailer)
        self.assertFalse(test_emailer.logged_in)
        self.assertEqual(mock_default.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_login(self, mock_smtplib):
        """
        Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates with Emailer.logged_in().
        """
        creds = self._make_credentials()
        test_emailer = Emailer(config=creds, delay_login=True)
        self.assertIsInstance(test_emailer, Emailer)
        test_emailer._login()
        mock_smtplib.return_value.login.assert_called_once_with(creds.sender_email,
                                                                creds.password)
        self.assertTrue(test_emailer.logged_in)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_logged_in(self, mock_smtplib):
        """
        Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates Emailer class
        property logged_in.
        """
        test_emailer = Emailer(config=self._make_credentials(), delay_login=False)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.logged_in)
        self.assertEqual(mock_smtplib.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_logout(self, mock_smtplib):
        """
        Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates SMTP.quit() when Emailer._logout()
        is called.
        """
        # the mocked instance of SMTP
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=self._make_credentials(), delay_login=False)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.logged_in)
        test_emailer._logout()
        self.assertFalse(test_emailer.logged_in)
        self.assertEqual(instance.quit.call_count, 1)

    @mock.patch('auto_emailer.emailer.Path')
    def test_emailer_email_template(self, mock_path):
        """
        Test class method: Emailer.email_template()
        opens, reads, and returns the given text file path.
        """
        instance = mock_path.return_value
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        test_emailer.email_template('test')
        self.assertEqual(instance.read_text.call_count, 1)

    @mock.patch('auto_emailer.emailer.Path')
    def test_emailer_email_template_error(self, mock_path):
        """
        Test class method: Emailer.email_template()
        raises FileNotFoundError if it cannot find the
        file from argument `template_path`.
        """
        instance = mock_path.return_value
        instance.read_text.side_effect = FileNotFoundError
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        with self.assertRaises(FileNotFoundError):
            test_emailer.email_template("test/bad/path")

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email(self, mock_smtplib):
        """
        Test class method: Emailer.send_email() is sent with
        passed arguments. Validate that SMTP.quit() is called
        after send_email().
        """
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        test_emailer.send_email(['test@gmail.com'],
                                'My test subject',
                                text="Hello"
                                )
        self.assertEqual(instance.sendmail.call_count, 1)
        self.assertEqual(instance.quit.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_attachments(self, mock_smtplib):
        """
        Test class method: Emailer.send_email() is sent with
        attachment. Validate that SMTP.quit() is called
        after send_email().
        """
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        test_emailer.send_email(['test@gmail.com'],
                                'My test subject',
                                text="Hello",
                                attach_files=[MOCK_USER_JSON_FILE]
                                )
        self.assertEqual(instance.sendmail.call_count, 1)

    @mock.patch('auto_emailer.emailer.Path')
    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_template(self, mock_smtplib, mock_path):
        """
        Test class method: Emailer.send_email() is sent with
        email template and template arguments. Validate path is used
        to read template and that SMTP.quit() is called
        after send_email().
        """
        instance_smtp = mock_smtplib.return_value
        instance_path = mock_path.return_value
        instance_path.read_text.return_value = "Testing templates {name}"
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        test_emailer.send_email(['test@gmail.com'],
                                'My test subject',
                                template_path='test',
                                template_args=dict(name='TESTING')
                                )
        self.assertEqual(instance_smtp.sendmail.call_count, 1)
        self.assertEqual(instance_path.read_text.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_disconnect(self, mock_smtplib):
        """
        Test class method: Emailer.send_email() re-attempt login and
        send_email if it encounters smtplib.SMTPConnectError() during
        initial send of email. Validate smtplib.SMTP() and
        smtplib.SMTP.sendmail() are called twice.
        """
        instance = mock_smtplib.return_value
        instance.sendmail.side_effect = smtplib.SMTPConnectError(421,
                                                                 'Cannot connect to SMTP server')
        test_emailer = Emailer(config=self._make_credentials(), delay_login=True)
        with self.assertRaises(smtplib.SMTPConnectError):
            test_emailer.send_email(['test@gmail.com'],
                                    'My test email',
                                    text="Hello"
                                    )
        self.assertEqual(instance.sendmail.call_count, 2)
        self.assertEqual(mock_smtplib.call_count, 2)


if __name__ == '__main__':
    unittest.main()
