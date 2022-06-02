import unittest

from tools.convertors import to_utf8


class TestConvertors(unittest.TestCase):
    def test_to_utf8_with_bytes(self):
        self.assertEqual(to_utf8(b'this is a byte string'), 'this is a byte string')

    def test_to_utf8_with_empty_bytes(self):
        self.assertEqual(to_utf8(b''), '')

    def test_to_utf8_with_string(self):
        self.assertEqual(to_utf8('this is a string'), 'this is a string')

    def test_to_utf8_with_empty_string(self):
        self.assertEqual(to_utf8(''), '')

    def test_to_utf8_with_number(self):
        with self.assertRaises(ValueError) as context:
            self.assertRaises(ValueError, to_utf8(12345))
        self.assertTrue('must be an instance of' in str(context.exception))

    def test_to_utf8_with_None(self):
        with self.assertRaises(ValueError) as context:
            self.assertRaises(ValueError, to_utf8(None))
        self.assertTrue('must be an instance of' in str(context.exception))
