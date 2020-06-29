class CouldNotReadConfigVariablesException(Exception):
    def __init__(self):
        self.value = "Could not read config variables file"

    def __str__(self):
        return repr(self.value)