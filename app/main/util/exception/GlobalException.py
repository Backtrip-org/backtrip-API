class StringTooLongException(Exception):
    def __init__(self, string_name, max_size):
        self.value = "{} is too long. max size is {} characters.".format(string_name, max_size)

    def __str__(self):
        return repr(self.value)
