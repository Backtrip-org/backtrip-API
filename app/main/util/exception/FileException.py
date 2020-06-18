class IdFileNotFoundException(Exception):
    def __init__(self, file_id):
        self.value = "File with id {} not found".format(file_id)

    def __str__(self):
        return repr(self.value)


class UploadFileNotFoundException(Exception):
    def __init__(self):
        self.value = "File to upload not found. Please add a body parameter named `file` containing the file to upload."

    def __str__(self):
        return repr(self.value)


class FileNotFoundException(Exception):
    def __init__(self):
        self.value = "File not found"

    def __str__(self):
        return repr(self.value)


class UnknownFileTypeException(Exception):
    def __init__(self, unknown_file_type):
        self.value = "Unknown file type: {}".format(unknown_file_type)

    def __str__(self):
        return repr(self.value)