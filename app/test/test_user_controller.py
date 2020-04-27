import unittest
import json

from app.test.base import BaseTestCase


def register_user(self, email='example@gmail.com'):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email=email,
            firstname='firstname',
            lastname='lastname',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self, email='example@gmail.com'):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password='123456'
        )),
        content_type='application/json'
    )


class TestUserController(BaseTestCase):
    def test_get_trips_should_return_trips_with_participants(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])

        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data).get('id')

        register_user(self, "friend@mail.com")
        invitation_payload = json.dumps(dict(email="friend@mail.com"))
        self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')

        get_trips_response = self.client.get('/user/{}/trips'.format(str(trip_id)), headers=headers)
        participants = json.loads(get_trips_response.data).get('data')[0].get('users_trips')

        self.assertEqual(get_trips_response.status_code, 200)
        self.assertEqual(len(participants), 2)
