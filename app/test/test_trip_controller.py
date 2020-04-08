import unittest
import json

from app.main.model.trip import Trip
from app.test.base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='example@gmail.com',
            firstname='firstname',
            lastname='lastname',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='example@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


class TestTripController(BaseTestCase):
    def test_create_trip_should_return_created(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        self.assertEqual(create_trip_response.status_code, 201)

    def test_create_trip_should_raise_conflict(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        create_second_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        self.assertEqual(create_second_trip_response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
