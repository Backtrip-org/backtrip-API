class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.value = "User already exists."

    def __str__(self):
        return repr(self.value)


class UserEmailNotFoundException(Exception):
    def __init__(self, user_email):
        self.value = "User with email '{}' does not exist.".format(user_email)

    def __str__(self):
        return repr(self.value)


class UserNotFoundException(Exception):
    def __init__(self, user_id):
        self.value = "User with id '{}' does not exist.".format(user_id)

    def __str__(self):
        return repr(self.value)


class UserDoesNotParticipatesToTrip(Exception):
    def __init__(self, user_id, trip_id):
        self.value = "User with id '{}' cannot access to trip id '{}'.".format(user_id, trip_id)

    def __str__(self):
        return repr(self.value)
