import json
import unittest
from unittest import mock
from pathlib import Path

import smtplib

from auto_emailer import Emailer, Message
from auto_emailer.config import credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_USER_JSON_FILE = DATA_DIR / 'mock_user_credentials.json'


def _get_mock_credentials(file):
    with file.open() as creds:
        return json.load(creds)


def _make_credentials():
    """Used for creating credentials.Credentials
    instance for test cases.
    """
    creds = _get_mock_credentials(MOCK_USER_JSON_FILE)
    return credentials.Credentials(**creds)


class TestEmailer(unittest.TestCase):

    def test_emailer_config_error(self):
        """Test initialization of Emailer with unknown config
        argument data type raises ValueError.
        """
        with self.assertRaises(ValueError):
            Emailer(config="My data")

    @mock.patch('auto_emailer.emailer.default_credentials')
    def test_emailer_none_error(self, mock_default):
        """Test initialization of Emailer raises ValueError if
        arguments are None and call to default.default_credentials()
        returns None.
        """
        mock_default.side_effect = ValueError
        with self.assertRaises(ValueError):
            Emailer()

    @mock.patch('auto_emailer.emailer.default_credentials')
    def test_emailer_defaults(self, mock_default):
        """Test initialization of Emailer() with default.default_credentials
        and validate smtplib is not called to login since delay_login argument
        is not passed.
        """
        mock_default.return_value = _make_credentials()
        test_emailer = Emailer()
        self.assertIsInstance(test_emailer, Emailer)
        self.assertFalse(test_emailer.connected)
        self.assertEqual(mock_default.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_login(self, mock_smtplib):
        """Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates with Emailer.connected().
        """
        creds = _make_credentials()
        test_emailer = Emailer(config=creds,
                               delay_login=True)
        self.assertIsInstance(test_emailer, Emailer)
        test_emailer._login()
        mock_smtplib.return_value.login.assert_called_once_with(creds.sender_email,
                                                                creds.password)
        self.assertTrue(test_emailer.connected)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_connected(self, mock_smtplib):
        """Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates Emailer class
        property connected.
        """
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=False)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.connected)
        self.assertEqual(mock_smtplib.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_logout(self, mock_smtplib):
        """Test class method: Emailer._login() authenticates SMTP client
        with passed credentials and validates SMTP.quit() when Emailer._logout()
        is called.
        """
        # the mocked instance of SMTP
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=False)
        self.assertIsInstance(test_emailer, Emailer)
        self.assertTrue(test_emailer.connected)
        test_emailer._logout()
        self.assertFalse(test_emailer.connected)
        self.assertEqual(instance.quit.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email(self, mock_smtplib):
        """Test class method: Emailer.send_email() is sent with
        passed arguments. Validate that SMTP.quit() is called
        after send_email().
        """
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=True)

        test_emailer.send_email('My test email',
                                test_emailer._config.sender_email,
                                'yotest@gmail.com')
        self.assertEqual(instance.sendmail.call_count, 1)
        self.assertEqual(instance.quit.call_count, 1)

    @mock.patch('auto_emailer.emailer.time.sleep')
    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_delay(self, mock_smtplib, mock_sleep):
        """Test class method: Emailer.send_email() is sent with
        passed arguments. Validate that time.sleep() is called
        with argument delay_send.
        """
        smtp_instance = mock_smtplib.return_value
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=True)

        test_emailer.send_email('My test email',
                                test_emailer._config.sender_email,
                                'yotest@gmail.com', delay_send=10)

        self.assertEqual(mock_sleep.call_count, 1)
        self.assertEqual(smtp_instance.sendmail.call_count, 1)
        self.assertEqual(smtp_instance.quit.call_count, 1)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_missing_message_args(self, mock_smtplib):
        """Test class method: Emailer.send_email() if provided string message
        but not `from_addr` or `from_addr` arguments than raise ValueError.
        Validate smtplib.SMTP.sendmail() is not called.
        """
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=True)
        with self.assertRaises(ValueError):
            test_emailer.send_email('Test',
                                    to_addrs='yotest@gmail.com')
        with self.assertRaises(ValueError):
                test_emailer.send_email('Test',
                                        from_addr='yotest@gmail.com')
        self.assertEqual(instance.sendmail.call_count, 0)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_message_type(self, mock_smtplib):
        """Test class method: Emailer.send_email() raises ValueError if
        message is not of type string or auto_emaier.emailer.Message.
        Validate smtplib.SMTP.sendmail() is not called.
        """
        instance = mock_smtplib.return_value
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=True)
        with self.assertRaises(ValueError):
            test_emailer.send_email({'Subject': 'Test'},
                                    to_addrs='yotest@gmail.com',
                                    from_addr='yotest@gmail.com')
        self.assertEqual(instance.sendmail.call_count, 0)

    @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    def test_emailer_send_email_disconnect(self, mock_smtplib):
        """Test class method: Emailer.send_email() re-attempt login and
        send_email if it encounters smtplib.SMTPConnectError() during
        initial send of email. Validate smtplib.SMTP() and
        smtplib.SMTP.sendmail() are called twice.
        """
        instance = mock_smtplib.return_value
        instance.sendmail.side_effect = smtplib.SMTPConnectError(421,
                                                                 'Cannot connect to SMTP server')
        test_emailer = Emailer(config=_make_credentials(),
                               delay_login=True)
        with self.assertRaises(smtplib.SMTPConnectError):
            test_emailer.send_email('My test email',
                                    test_emailer._config.sender_email,
                                    'yotest@gmail.com')
        self.assertEqual(instance.sendmail.call_count, 2)
        self.assertEqual(mock_smtplib.call_count, 2)


class TestMessage(unittest.TestCase):

    @mock.patch('auto_emailer.emailer.MIMEMultipart')
    def test_emailer_message_message(self, mock_multipart):
        """Test class method: Message.__int__ creates MIMEMultipart
        message. Validate MIMEMultipart is called and the Message.message
        attribute is MIMEMultipart.
        """
        instance_multipart = mock_multipart.return_value
        test_message = Message('my_email@gmail.com',
                               ['my_friend@gmail.com'],
                               'Hello Friend!')
        self.assertEqual(mock_multipart.call_count, 1)
        self.assertEqual(test_message.message, instance_multipart)

    @mock.patch('auto_emailer.emailer.MIMEMultipart')
    def test_emailer_message_str_override(self, mock_multipart):
        """Test class method: Message.__str__ returns MIMEMultipart message
        as_string(). Validate MIMEMultipart is called and the Message.message
        attribute is MIMEMultipart. Validate MIMEMultipart.as_string() is
        called.
        """
        instance_multipart = mock_multipart.return_value
        test_message = Message('my_email@gmail.com',
                               ['my_friend@gmail.com'],
                               'Hello Friend!')
        test_message_string = test_message.__str__()
        self.assertEqual(mock_multipart.call_count, 1)
        self.assertEqual(test_message.message, instance_multipart)
        self.assertEqual(instance_multipart.as_string.call_count, 1)

    @mock.patch('auto_emailer.emailer.MIMEText')
    @mock.patch('auto_emailer.emailer.MIMEMultipart')
    def test_emailer_message_draft_message_text(self, mock_multipart, mock_text):
        """Test class method: Message.message returns MIMEMultipart message
        with MIMEText attached. Validate MIMEMultipart is called and the
        Message.message attribute is MIMEMultipart. Validate
        MIMEMultipart.attach is called.
        """
        instance_multipart = mock_multipart.return_value
        instance_text = mock_text.return_value
        test_message = Message('my_email@gmail.com',
                               ['my_friend@gmail.com'],
                               'Hello Friend!')
        test_message.draft_message(text='Hi Friend!')

        calls = [mock.call.__setitem__('From', 'my_email@gmail.com'),
                 mock.call.__setitem__('To', 'my_friend@gmail.com'),
                 mock.call.__setitem__('BCC', ''),
                 mock.call.__setitem__('CC', ''),
                 mock.call.__setitem__('Subject', 'Hello Friend!'),
                 mock.call.attach(instance_text)]

        instance_multipart.assert_has_calls(calls)
        self.assertEqual(mock_multipart.call_count, 1)
        self.assertEqual(test_message.message, instance_multipart)

    @mock.patch('auto_emailer.emailer.Path')
    @mock.patch('auto_emailer.emailer.MIMEMultipart')
    def test_emailer_message_body_template(self, mock_multipart, mock_path):
        """Test class method: Message.body_template()
        opens, reads, and returns the given text file path.
        """
        instance_path = mock_path.return_value
        test_message = Message('my_email@gmail.com',
                               ['my_friend@gmail.com'],
                               'Hello Friend!')
        test_message.body_template('test')
        self.assertEqual(instance_path.read_text.call_count, 1)

    @mock.patch('auto_emailer.emailer.Path')
    @mock.patch('auto_emailer.emailer.MIMEMultipart')
    def test_emailer_message_body_template_error(self, mock_multipart, mock_path):
        """Test class method: Message.body_template()
        raises FileNotFoundError if it cannot find the
        file from argument `template_path`.
        """
        instance_path = mock_path.return_value
        instance_path.read_text.side_effect = FileNotFoundError
        test_message = Message('my_email@gmail.com',
                               ['my_friend@gmail.com'],
                               'Hello Friend!')

        with self.assertRaises(FileNotFoundError):
            test_message.body_template("test/bad/path")

    # @mock.patch('auto_emailer.emailer.smtplib.SMTP')
    # def test_emailer_send_email_attachments(self, mock_smtplib):
    #     """Test class method: Emailer.send_email() is sent with
    #     attachment. Validate that SMTP.quit() is called
    #     after send_email().
    #     """
    #     instance = mock_smtplib.return_value
    #     test_emailer = Emailer(config=self._make_credentials(),
    #                            delay_login=True)
    #     test_emailer.send_email(['test@gmail.com'],
    #                             'My test subject',
    #                             text="Hello",
    #                             attach_files=[MOCK_USER_JSON_FILE]
    #                             )
    #     self.assertEqual(instance.sendmail.call_count, 1)

    # @mock.patch('auto_emailer.emailer.Path')
    # @mock.patch('auto_emailer.emailer.MIMEMultipart')
    # def test_emailer_send_email_template(self, mock_smtplib, mock_path):
    #     """Test class method: Emailer.send_email() is sent with
    #     email template and template arguments. Validate path is used
    #     to read template and that SMTP.quit() is called
    #     after send_email().
    #     """
    #     instance_smtp = mock_smtplib.return_value
    #     instance_path = mock_path.return_value
    #     instance_path.read_text.return_value = "Testing templates {name}"
    #     test_emailer = Emailer(config=self._make_credentials(),
    #                            delay_login=True)
    #     test_emailer.send_email(['test@gmail.com'],
    #                             'My test subject',
    #                             template_path='test',
    #                             template_args=dict(name='TESTING')
    #                             )
    #     self.assertEqual(instance_smtp.sendmail.call_count, 1)
    #     self.assertEqual(instance_path.read_text.call_count, 1)




if __name__ == '__main__':
    unittest.main()
