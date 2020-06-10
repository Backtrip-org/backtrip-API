from enum import Enum

from app.main.util.exception.FileException import UnknownFileTypeException


class FileType(Enum):
    Document = 0
    Photo = 1

    @staticmethod
    def from_string(string_file_type):
        if not FileType.__dict__.__contains__(string_file_type):
            raise UnknownFileTypeException(string_file_type)
        return FileType.__dict__[string_file_type];
