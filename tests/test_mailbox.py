import os
import unittest
from io import StringIO
from unittest.mock import Mock, MagicMock, patch, ANY

from processors.mailbox import process_mailbox
from tests.test_config import TestConfig


class TestMailbox(unittest.TestCase):
    dummy_os_env = {
        'EMAIL_SVC_IMAP': 'mock EMAIL_SVC_IMAP',
        'EMAIL_SVC_SMTP': 'mock EMAIL_SVC_SMTP',
        'EMAIL_ACCOUNT': 'mock EMAIL_ACCOUNT',
        'EMAIL_PASSWD': 'mock EMAIL_PASSWD',
        'EMAIL_FOLDER': 'mock EMAIL_FOLDER',
        'SPAM_URL': 'mock SPAM_URL',
        'SPAM_LOGIN_PASSWD': 'mock SPAM_URL'
    }

    def test_process_mailbox_no_msg_found(self):
        mailbox_mock = Mock()
        mailbox_mock.search = MagicMock(return_value=('KO', None))
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            process_mailbox(mailbox_mock)
            self.assertEqual(mock_stdout.getvalue(), "No messages found!\n")

    @patch('smtplib.SMTP_SSL')
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_process_mailbox_nothing_to_do(self, mock_smtp):
        mailbox_mock = Mock()
        mailbox_mock.search = MagicMock(return_value=('OK', [b'']))
        mailbox_mock.fetch = MagicMock(return_value=('KO', None))
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            process_mailbox(mailbox_mock)
            self.assertEquals('  > Nothing to do for now\n', mock_stdout.getvalue())

    @patch('smtplib.SMTP_SSL')
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_process_mailbox_host_error_getting_message(self, mock_smtp):
        mailbox_mock = Mock()
        mailbox_mock.search = MagicMock(return_value=('OK', [b'1']))
        mailbox_mock.fetch = MagicMock(return_value=('KO', None))
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            process_mailbox(mailbox_mock)
            self.assertEquals("ERROR getting message b'1'\n", mock_stdout.getvalue())

    @patch('smtplib.SMTP_SSL', MagicMock(return_value=ANY))
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    @patch('spamcop.spamcop_http.send_to_spamcop', MagicMock(return_value=ANY))
    def test_process_mailbox_success(self):
        mailbox_mock = Mock()
        mailbox_mock.search = MagicMock(return_value=('OK', [b'1']))
        mailbox_mock.fetch = MagicMock(return_value=('OK', [(b'1 (RFC822 {12345}',
                                                             b'Message-ID: <YQBqsX9CgeS3T7yybFJG>\r\nSubject: dummy '
                                                             b'e-mail\r\nFrom: anonymous '
                                                             b'<sender@mail-service.tld>\r\nTo: '
                                                             b'recipient@another-mail-service.tld\r\nContent-Type: '
                                                             b'multipart/alternative; '
                                                             b'boundary="0000000000003X6JsL6wrefZnFIa\r\n--\r'
                                                             b'\nContent-Type: text/plain; '
                                                             b'charset="UTF-8"\r\n--\r\nContent-Type: text/html; '
                                                             b'charset="UTF-8"\r\nmail body is '
                                                             b'here\r\n--0000000000003X6JsL6wrefZnFIa\r\n'),
                                                            b' FLAGS (\\Seen))']))
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            process_mailbox(mailbox_mock)
            self.assertEqual('    [*] msg 01: dummy e-mail\n', mock_stdout.getvalue())
