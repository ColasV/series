import unittest
from lib.betaseries import extension

__author__ = 'vignesn'


class TestExtension(unittest.TestCase):
    def test_extension_zip(self):
        filename = 'fichier.zip'
        self.assertEqual('zip', extension(filename))

    def test_none_extension(self):
        filename = 'fichier'
        self.assertEqual(None, extension(filename))

    def test_multiple_extension(self):
        filename = 'fichier.test.zip.tar'
        self.assertEqual('tar', extension(filename))

    def test_path_extension(self):
        filename = '/path/to/a/file.tar'
        self.assertEqual('tar', extension(filename))

    def test_null_path(self):
        filename = ''
        self.assertEqual(None, extension(filename))

if __name__ == '__main__':
    unittest.main()