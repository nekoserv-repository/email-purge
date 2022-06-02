import os
import unittest
from io import StringIO
from unittest.mock import patch

from config.configservice import ConfigService


class TestConfig(unittest.TestCase):
    mock_os_env = {
        'EMAIL_SVC_IMAP': 'mock EMAIL_SVC_IMAP',
        'EMAIL_SVC_SMTP': 'mock EMAIL_SVC_SMTP',
        'EMAIL_ACCOUNT': 'mock EMAIL_ACCOUNT',
        'EMAIL_PASSWD': 'mock EMAIL_PASSWD',
        'EMAIL_FOLDER': 'mock EMAIL_FOLDER',
        'SPAM_URL': 'mock SPAM_URL',
        'SPAM_LOGIN_PASSWD': 'mock SPAM_LOGIN_PASSWD'
    }

    @patch.dict(os.environ, mock_os_env, clear=True)
    def test_check_runtime_cfg_all_env_vars_are_set(self):
        for e in self.mock_os_env.keys():
            ConfigService.get(e)

    @patch.dict(os.environ, {
        'EMAIL_SVC_IMAP': 'a',
        'EMAIL_SVC_SMTP': 'b',
        'EMAIL_ACCOUNT': 'c'
    }, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_runtime_cfg_missing_at_least_one_env_var(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            for e in self.mock_os_env.keys():
                ConfigService.get(e)
        self.assertEqual(context.exception.code, 1)
        for e in ['EMAIL_PASSWD', 'EMAIL_FOLDER', 'SPAM_URL', 'SPAM_LOGIN_PASSWD']:
            self.assertTrue('runtime parameter "' + e + '" is not set\n' in mock_stdout.getvalue())

    @patch.dict(os.environ, {}, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_check_runtime_cfg_missing_all_env_vars(self, mock_stdout):
        with self.assertRaises(SystemExit) as context:
            for e in self.mock_os_env.keys():
                ConfigService.get(e)
        self.assertEqual(context.exception.code, 1)
        for e in self.mock_os_env.keys():
            self.assertTrue('runtime parameter "' + e + '" is not set' in mock_stdout.getvalue())
