import unittest
import json

from app.main.model.trip import Trip
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

    def test_create_step_should_return_created(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 201)

    def test_create_step_should_raise_bad_request(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 400)

    def test_create_step_should_raise_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id + 1)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 404)

    def test_create_step_should_raise_unauthorized(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00'))
        headers['Authorization'] = ''
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 401)

    def test_invite_to_trip_should_return_no_content(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        register_user(self, participant_email)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 204)

    def test_invite_to_trip_should_return_bad_request(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 400)

    def test_invite_to_trip_should_return_unauthorized(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        register_user(self, participant_email)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        headers['Authorization'] = ''
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 401)

    def test_invite_to_trip_should_return_not_found(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        register_user(self, participant_email)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id + 1)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 404)
    def test_get_step_should_return_ok(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data.decode())['id']
        step = self.client.get('/trip/{}/step/{}'.format(str(trip_id), str(step_id)), headers=headers,
                               data=step_payload, content_type='application/json')
        self.assertEqual(step.status_code, 200)

    def test_get_uncreated_step_should_return_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data.decode())['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data.decode())['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data.decode())['id']
        step = self.client.get('/trip/{}/step/{}'.format(str(trip_id), str(step_id + 1)), headers=headers,
                               data=step_payload, content_type='application/json')
        self.assertEqual(step.status_code, 404)


if __name__ == '__main__':
    unittest.main()
