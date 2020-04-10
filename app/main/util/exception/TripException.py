class TripAlreadyExistsException(Exception):
    def __init__(self):
        self.value = "Trip already exists. Please choose a new name."

    def __str__(self):
        return repr(self.value)


class TripNotFoundException(Exception):
    def __init__(self, trip_id):
        self.value = "Trip with id {} does not exist.".format(trip_id)

    def __str__(self):
        return repr(self.value)
