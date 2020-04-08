class TripAlreadyExistsException(Exception):
    def __init__(self):
        self.value = "Trip already exists. Please choose a new name."

    def __str__(self):
        return repr(self.value)
