class StringLengthOutOfRangeException(Exception):
    def __init__(self, string_name, min_size, max_size):
        self.value = "{} must be between {} and {} characters.".format(string_name, min_size, max_size)

    def __str__(self):
        return repr(self.value)
