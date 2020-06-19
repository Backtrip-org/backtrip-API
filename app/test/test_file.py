import unittest

from app.main.model.file.file_type import FileType
from app.main.util.exception.FileException import UnknownFileTypeException
from app.test.base import BaseTestCase

file_type_enum = [(FileType.Document, 'Document'), (FileType.Photo, 'Photo')]


class MyTestCase(BaseTestCase):
    def test_string_file_type_returns_enum_file_type(self):
        for enum_file_type, string_file_type in file_type_enum:
            with self.subTest():
                self.assertEqual(enum_file_type, FileType.from_string(string_file_type))

    def test_unknown_string_file_type_raise_exception(self):
        with self.assertRaises(UnknownFileTypeException):
            FileType.from_string('Unknown type')


if __name__ == '__main__':
    unittest.main()
