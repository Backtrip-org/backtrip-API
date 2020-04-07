class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.value = "User already exists."

    def __str__(self):
        return repr(self.value)