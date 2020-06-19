class BusinessNotFoundException(Exception):
    def __init__(self, place_id):
        self.value = "Could not find a business for the place with id ".format(place_id)

    def __str__(self):
        return repr(self.value)


class ReviewsNotFoundException(Exception):
    def __init__(self, business_id):
        self.value = "Could not find reviews for the business with id ".format(business_id)

    def __str__(self):
        return repr(self.value)


class NotEnoughReviewsException(Exception):
    def __init__(self):
        self.value = "Not enough reviews to calculate rating"

    def __str__(self):
        return repr(self.value)