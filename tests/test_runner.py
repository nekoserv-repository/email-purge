import os
from imaplib import IMAP4
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock

from processors.runner import Runner
from tests.test_config import TestConfig


class TestRunner(TestCase):

    def test__signal_handler(self):
        with patch('processors.runner.Runner.mailbox', new_callable=PropertyMock) as mb, \
                self.assertRaises(SystemExit) as context, \
                patch('sys.stdout', new=StringIO()) as mock_stdout:
            mb.return_value.socket.return_value.fileno.return_value = 42
            ep = Runner()
            ep._signal_handler()
        self.assertEqual('! caught exit signal - farewell\n', mock_stdout.getvalue())
        self.assertEqual(context.exception.code, 0)

    @patch('processors.runner.IMAP4_SSL', MagicMock(side_effect=IMAP4.error()))
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_mail_loop_failed_login(self):
        with self.assertRaises(SystemExit) as context, \
                patch('sys.stdout', new=StringIO()) as mock_stdout:
            ep = Runner()
            ep.mail_loop()
        self.assertEqual('FATAL : login to mailbox failed \n', mock_stdout.getvalue())
        self.assertEqual(context.exception.code, 1)

    @patch('processors.runner.IMAP4_SSL')
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_mail_loop_open_mailbox_failed(self, mock_imaplib):
        mock_imaplib.return_value.select.return_value = ('KO', 'dummy')
        with self.assertRaises(SystemExit) as context, \
                patch('sys.stdout', new=StringIO()) as mock_stdout:
            ep = Runner()
            ep.mail_loop()
        self.assertEqual(context.exception.code, 1)
        self.assertEqual('ERROR: Unable to open mailbox KO\n', mock_stdout.getvalue())

    @patch('processors.runner.IMAP4_SSL', MagicMock())
    @patch('processors.runner.sleep', MagicMock())
    @patch('processors.runner.process_mailbox', MagicMock())
    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_mail_loop_success(self):
        with patch('processors.runner.Runner.mailbox', new_callable=PropertyMock) as mb, \
                patch('sys.stdout', new=StringIO()) as mock_stdout:
            mb.return_value.select.return_value = ('OK', 'dummy')
            ep = Runner()
            ep._call_imap_server()
            self.assertEqual('> Opening mailbox...\n> Done.\n~ waiting 10 min\n', mock_stdout.getvalue())
