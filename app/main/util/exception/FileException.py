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
