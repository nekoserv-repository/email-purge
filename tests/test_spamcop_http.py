import os
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, MagicMock, ANY

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests_html import HTML, HTMLSession

from spamcop.spamcop_http import get_headers, wait, get_prefill, get_all_forms, send_post, send_get, send_to_spamcop
from tests.test_config import TestConfig


class Response:
    def __init__(
            self,
            html,
            ok=True
    ):
        self._set_html(html)
        self._set_ok(ok)

    def _set_html(self, html):
        self.html = HTML(html=html)

    def _set_ok(self, v):
        self.ok = v

    def close(self):
        return


class HtmlResponse(Response):
    pass


class TestSpamCopHttp(TestCase):
    response_class = HtmlResponse

    html = '<form action="dummy">' \
           '<input name="input1" value="value1"/><input name="input2" value="value2"/>' \
           '<textarea name="tr1" value="value3"></textarea><textarea name="tr2" value="value4"></textarea>' \
           '</form>'

    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('spamcop.spamcop_http.send_get', MagicMock(return_value=response_class(html=html)))
    @patch('spamcop.spamcop_http.send_post')
    @patch('spamcop.spamcop_http.wait', MagicMock())
    def test_send_to_spamcop(self, mock_post, mock_stdout):
        mock_post.return_value.url.return_value = ANY
        send_to_spamcop(ANY)
        self.assertEquals('  > connecting to SpamCop\n  ~ sending spam\n  ~ filling spam report\n  ~ done\n',
                          mock_stdout.getvalue())

    @patch('spamcop.spamcop_http.get_headers', MagicMock(return_value=ANY))
    @patch('spamcop.spamcop_http.HTMLSession.get', MagicMock(return_value=response_class(html=html, ok=True)))
    def test_send_get_ok(self):
        r = send_get(HTMLSession(), ANY)
        self.assertIsNotNone(r)

    @patch('spamcop.spamcop_http.get_headers', MagicMock(return_value=ANY))
    @patch('spamcop.spamcop_http.HTMLSession.get', MagicMock(return_value=response_class(html=html, ok=False)))
    def test_send_get_error(self):
        with self.assertRaises(Exception) as context:
            send_get(HTMLSession(), ANY)
        self.assertEqual(context.exception.args[0], 'not connected!')

    @patch('spamcop.spamcop_http.get_headers', MagicMock(return_value=ANY))
    @patch('spamcop.spamcop_http.HTMLSession.post', MagicMock(return_value=response_class(html=html, ok=True)))
    def test_send_post_ok(self):
        r = send_post(HTMLSession(), ANY, ANY)
        self.assertIsNotNone(r)

    @patch('spamcop.spamcop_http.get_headers', MagicMock(return_value=ANY))
    @patch('spamcop.spamcop_http.HTMLSession.post', MagicMock(return_value=response_class(html=html, ok=False)))
    def test_send_post_error(self):
        with self.assertRaises(Exception) as context:
            send_post(HTMLSession(), ANY, ANY)
        self.assertEqual(context.exception.args[0], 'not connected!')

    def test_get_all_forms(self):
        rc = self.response_class(html=self.html)
        r = get_all_forms(rc)
        self.assertTrue(isinstance(r, ResultSet))
        for c in r[0].contents:
            self.assertTrue(str(c) in self.html)

    def test_get_prefill(self):
        soup = BeautifulSoup(self.html, "html.parser")
        form = soup.find_all("form")
        r = get_prefill(form[0])
        self.assertEqual(r, {'input1': 'value1', 'input2': 'value2', 'tr1': 'value3', 'tr2': 'value4'})

    @patch('spamcop.spamcop_http.sleep', MagicMock())
    def test_wait(self):
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            wait(10)
            self.assertEqual('  - wait 10 seconds..........\n', mock_stdout.getvalue())

    @patch.dict(os.environ, TestConfig.mock_os_env, clear=True)
    def test_get_headers(self):
        self.assertEqual({'Authorization': 'Basic bW9jayBTUEFNX0xPR0lOX1BBU1NXRA=='}, get_headers())
