import os
import requests

from app.main.config import config_variables
from app.main.service.pycountry_service import country_to_isocode
from app.main.util.exception.RatingException import BusinessNotFoundException, ReviewsNotFoundException, \
    NotEnoughReviewsException

url = 'https://api.yelp.com/v3/businesses'
api_key = config_variables.get('yelp_api_key')


def get_rating(place):
    if place is None:
        raise ValueError("Place object must not be None")

    try:
        business_id = get_business_id(place)
        reviews = get_reviews(business_id)
        return calculate_average_rating(reviews)
    except (BusinessNotFoundException, ReviewsNotFoundException):
        return None


def get_business_id(place):
    country_code = country_to_isocode(place.country)

    params = {
        'name': place.name,
        'address1': place.street,
        'city': place.city,
        'state': country_code,
        'country': country_code
    }
    headers = {'Authorization': api_key}

    request = requests.get('{}/matches'.format(url), params=params, headers=headers)
    businesses = request.json().get('businesses')

    if request.status_code != 200 or len(businesses) < 1:
        raise BusinessNotFoundException(place.id)

    return businesses[0].get('id')


def get_reviews(business_id):
    headers = {'Authorization': api_key}
    request = requests.get('{}/{}/reviews'.format(url, business_id), headers=headers)

    if request.status_code != 200:
        raise ReviewsNotFoundException(business_id)

    return request.json().get('reviews')


def calculate_average_rating(reviews):
    if len(reviews) < 1:
        raise NotEnoughReviewsException()
    rating_sum = sum(review.get('rating') for review in reviews)
    return round(rating_sum / len(reviews), 2)
