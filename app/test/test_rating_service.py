import unittest

import responses

from app.main.model.place.place import Place
from app.main.model.step.step import Step
from app.main.service.rating_service import calculate_average_rating, url, get_business_id, get_reviews, get_rating
from app.main.util.exception.RatingException import NotEnoughReviewsException, BusinessNotFoundException, \
    ReviewsNotFoundException
from app.test.base import BaseTestCase

reviews_to_average_rating = [
    ([{'id': 1, 'rating': 3}, {'id': 2, 'rating': 5}, {'id': 3, 'rating': 4}], 4),
    ([{'id': 1, 'rating': 1}, {'id': 2, 'rating': 3}, {'id': 3, 'rating': 4}], 2.67),
    ([{'id': 1, 'rating': 2}, {'id': 2, 'rating': 2}, {'id': 3, 'rating': 2}], 2)
]


class MyTestCase(BaseTestCase):
    def test_calculate_average_rating_return_average_rating(self):
        for reviews, average in reviews_to_average_rating:
            with self.subTest():
                self.assertEqual(average, calculate_average_rating(reviews))

    def test_calculate_average_rating_raise_exception(self):
        with self.assertRaises(NotEnoughReviewsException):
            calculate_average_rating([])

    @responses.activate
    def test_get_business_id_should_return_business_id(self):
        responses.add(
            responses.GET,
            '{}/matches'.format(url),
            status=200,
            json={
                "businesses": [
                    {
                        "id": "EDjIDq3VGlDQAxtdOslPCA",
                        "alias": "cracker-barrel-old-country-store-hattiesburg",
                        "name": "Cracker Barrel Old Country Store",
                    }
                ]
            }
        )
        self.assertEqual('EDjIDq3VGlDQAxtdOslPCA', get_business_id(Place()))

    @responses.activate
    def test_get_business_id_with_no_result_should_raise_exception(self):
        responses.add(
            responses.GET,
            '{}/matches'.format(url),
            status=200,
            json={
                "businesses": []
            }
        )
        with self.assertRaises(BusinessNotFoundException):
            get_business_id(Place(id=1))

    @responses.activate
    def test_get_business_id_with_api_error_status_should_raise_exception(self):
        responses.add(
            responses.GET,
            '{}/matches'.format(url),
            status=400,
            json={}
        )
        with self.assertRaises(BusinessNotFoundException):
            get_business_id(Place(id=1))

    @responses.activate
    def test_get_reviews_should_return_3_reviews(self):
        business_id = 1
        responses.add(
            responses.GET,
            '{}/{}/reviews'.format(url, business_id),
            status=200,
            json={
                "reviews": [
                    {
                        "id": "mLmKOhUW87byM7lsMDDz_w",
                        "rating": 3,
                    },
                    {
                        "id": "Al1G6S7IZcIVFdSAA-fKgw",
                        "rating": 1,
                    },
                    {
                        "id": "3uxMqhNcZdmbt4p08gSZyQ",
                        "rating": 2,
                    }
                ],
                "total": 46
            }
        )
        self.assertEqual([
            {
                "id": "mLmKOhUW87byM7lsMDDz_w",
                "rating": 3,
            },
            {
                "id": "Al1G6S7IZcIVFdSAA-fKgw",
                "rating": 1,
            },
            {
                "id": "3uxMqhNcZdmbt4p08gSZyQ",
                "rating": 2,
            }
        ], get_reviews(business_id))

    @responses.activate
    def test_get_reviews_should_return_0_reviews(self):
        business_id = 1
        responses.add(
            responses.GET,
            '{}/{}/reviews'.format(url, business_id),
            status=200,
            json={
                "reviews": [],
                "total": 0
            }
        )
        self.assertEqual([], get_reviews(business_id))

    @responses.activate
    def test_get_reviews_with_api_error_should_raise_exception(self):
        business_id = 1
        responses.add(
            responses.GET,
            '{}/{}/reviews'.format(url, business_id),
            status=400,
            json={}
        )
        with self.assertRaises(ReviewsNotFoundException):
            get_reviews(business_id)

    def test_get_rating_with_None_place_return_None(self):
        step = Step()
        with self.assertRaises(ValueError):
            get_rating(step.start_address)

    @responses.activate
    def test_get_rating_should_return_rating(self):
        business_id = 'EDjIDq3VGlDQAxtdOslPCA'
        responses.add(
            responses.GET,
            '{}/matches'.format(url),
            status=200,
            json={
                "businesses": [
                    {
                        "id": business_id,
                        "alias": "cracker-barrel-old-country-store-hattiesburg",
                        "name": "Cracker Barrel Old Country Store",
                    }
                ]
            }
        )
        responses.add(
            responses.GET,
            '{}/{}/reviews'.format(url, business_id),
            status=200,
            json={
                "reviews": [
                    {
                        "id": "mLmKOhUW87byM7lsMDDz_w",
                        "rating": 3,
                    },
                    {
                        "id": "Al1G6S7IZcIVFdSAA-fKgw",
                        "rating": 1,
                    },
                    {
                        "id": "3uxMqhNcZdmbt4p08gSZyQ",
                        "rating": 2,
                    }
                ],
                "total": 46
            }
        )

        self.assertEqual(2, get_rating(Place()))


if __name__ == '__main__':
    unittest.main()
