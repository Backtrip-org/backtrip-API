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


class TestTripController(BaseTestCase):
    def test_create_trip_should_return_created(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        self.assertEqual(create_trip_response.status_code, 201)

    def test_create_trip_should_raise_conflict(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        create_second_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        self.assertEqual(create_second_trip_response.status_code, 409)

    def test_create_trip_with_too_long_name_should_raise_bad_request(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        payload = json.dumps(dict(name='this trip name is too long', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        create_trip_response_data = json.loads(create_trip_response.data)
        self.assertEqual(create_trip_response.status_code, 400)
        self.assertEqual(create_trip_response_data.get('message'), 'Name must be between 2 and 20 characters.')

    def test_create_step_should_return_created(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 201)

    def test_create_step_with_too_long_name_should_raise_bad_request(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 400)

    def test_create_step_with_wrong_type_should_raise_bad_request(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00', type='Unknown'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 400)
        self.assertEqual(json.loads(create_step_response.data).get('message'), "Step with type Unknown does not exist.")

    def test_create_step_should_raise_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id + 1)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 404)

    def test_create_step_should_raise_unauthorized(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='s' * 30, start_datetime='2020-04-10 21:00:00', type='Base'))
        headers['Authorization'] = ''
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        self.assertEqual(create_step_response.status_code, 401)

    def test_invite_to_trip_should_return_no_content(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        register_user(self, participant_email)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 204)

    def test_invite_to_trip_should_return_bad_request(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 400)

    def test_invite_to_trip_should_return_unauthorized(self):
        register_user(self)
        participant_email = 'participant@mail.com'
        register_user(self, participant_email)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
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
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        invitation_payload = json.dumps(dict(email=participant_email))
        invitation_response = self.client.post('/trip/{}/invite'.format(str(trip_id + 1)), headers=headers,
                                               data=invitation_payload, content_type='application/json')
        self.assertEqual(invitation_response.status_code, 404)

    def test_get_step_should_return_ok(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        step = self.client.get('/trip/{}/step/{}'.format(str(trip_id), str(step_id)), headers=headers,
                               data=step_payload, content_type='application/json')
        self.assertEqual(step.status_code, 200)

    def test_get_uncreated_step_should_return_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-04-10 21:00:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        step = self.client.get('/trip/{}/step/{}'.format(str(trip_id), str(step_id + 1)), headers=headers,
                               data=step_payload, content_type='application/json')
        self.assertEqual(step.status_code, 404)

    def test_get_timeline_should_return_ok(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        get_timeline_response = self.client.get('/trip/{}/timeline'.format(str(trip_id)), headers=headers)
        self.assertEqual(get_timeline_response.status_code, 200)

    def test_get_other_trip_timeline_should_return_unauthorized(self):
        register_user(self, "user1@mail.com")
        register_user(self, "user2@mail.com")
        login_response_user_1 = login_user(self, "user1@mail.com")
        login_response_user_2 = login_user(self, "user2@mail.com")
        auth_headers_user_1 = dict(Authorization=json.loads(login_response_user_1.data)['Authorization'])
        auth_headers_user_2 = dict(Authorization=json.loads(login_response_user_2.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=auth_headers_user_1, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        get_timeline_response = self.client.get('/trip/{}/timeline'.format(str(trip_id)), headers=auth_headers_user_2)
        self.assertEqual(get_timeline_response.status_code, 401)
        self.assertEqual(json.loads(get_timeline_response.data).get('message'),
                         'Unauthorized, you can\'t access this trip')

    def test_get_unknown_trip_timeline_should_return_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        get_timeline_response = self.client.get('/trip/{}/timeline'.format(str(trip_id + 1)), headers=headers)
        self.assertEqual(get_timeline_response.status_code, 404)

    def test_add_participant_to_step_should_return_200(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        self.assertEqual(add_participant_response.status_code, 200)

    def test_add_participant_to_step_should_return_401_invalid_token(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        add_participant_payload = json.dumps(dict(id=user_id))
        headers = dict(Authorization='Wrong key')
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        self.assertEqual(add_participant_response.status_code, 401)

    def test_add_participant_to_step_should_return_401_user_unknown(self):
        register_user(self)
        user_id = json.loads(register_user(self, 'second_user@mail.fr').data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        self.assertEqual(add_participant_response.status_code, 401)

    def test_add_participant_to_step_should_return_404(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id'] + 1
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        self.assertEqual(add_participant_response.status_code, 404)

    def test_get_personal_timeline_should_return_ok(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id'] + 1
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        personal_timeline_response = self.client.get('trip/{}/timeline/personal'.format(str(trip_id)),
                                                     headers=headers,
                                                     content_type='application/json')
        self.assertEqual(personal_timeline_response.status_code, 200)

    def test_get_personal_timeline_should_return_404(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id'] + 1
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post(
            'trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
            headers=headers, data=add_participant_payload,
            content_type='application/json')
        personal_timeline_response = self.client.get('trip/{}/timeline/personal'.format(str(3)),
                                                     headers=headers,
                                                     content_type='application/json')
        self.assertEqual(personal_timeline_response.status_code, 404)

    def test_create_expense_should_return_ok(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        expense_payload = json.dumps(dict(cost=150.50, name="test", user_id=user_id, trip_id=trip_id))
        create_expense_response = \
            self.client.post('/trip/{}/expense'.format(str(trip_id)), headers=headers, data=expense_payload,
                             content_type='application/json')
        self.assertEqual(create_expense_response.status_code, 200)

    def test_create_reimbursement_should_return_ok(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        expense_payload = json.dumps(dict(cost=150.50, user_id=user_id, trip_id=trip_id))
        create_expense_response = \
            self.client.post('/trip/{}/expense'.format(str(trip_id)), headers=headers, data=expense_payload,
                             content_type='application/json')
        expense_id = json.loads(create_expense_response.data)['id']
        reimbursement_payload = json.dumps(
            dict(cost=100.50, expense_id=expense_id, emitter_id=user_id, payee_id=user_id, trip_id=trip_id))
        create_reimbursement_response = \
            self.client.post('/trip/{}/reimbursement'.format(str(trip_id)), headers=headers, data=reimbursement_payload,
                             content_type='application/json')
        self.assertEqual(create_reimbursement_response.status_code, 200)

    def test_get_expenses_should_return_ok(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        expense_payload = json.dumps(dict(cost=150.50, user_id=user_id, trip_id=trip_id))
        create_expense_response = \
            self.client.post('/trip/{}/expense'.format(str(trip_id)), headers=headers, data=expense_payload,
                             content_type='application/json')
        expense_payload = json.dumps(dict(user_id=user_id))
        expenses = self.client.get('/trip/{}/user/{}/expenses'.format(str(trip_id), str(user_id)), headers=headers,
                                   data=expense_payload, content_type='application/json')
        self.assertEqual(expenses.status_code, 200)

    def test_remove_user_from_step_should_return_ok(self):
        user_id = json.loads(register_user(self).data)['id']
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        trip_payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=trip_payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        step_payload = json.dumps(dict(name='step', start_datetime='2020-05-03 21:20:00', type='Base'))
        create_step_response = self.client.post('/trip/{}/step'.format(str(trip_id)), headers=headers,
                                                data=step_payload, content_type='application/json')
        step_id = json.loads(create_step_response.data)['id']
        add_participant_payload = json.dumps(dict(id=user_id))
        add_participant_response = self.client.post('trip/{}/step/{}/participant'.format(str(trip_id), str(step_id)),
                                                    headers=headers, data=add_participant_payload,
                                                    content_type='application/json')
        remove_user_from_step_response = self.client.delete('trip/{}/step/{}/user/{}/leave'.format(str(trip_id),
                                                                                                   str(step_id),
                                                                                                   str(user_id)),
                                                            headers=headers,
                                                            content_type='application/json')
        self.assertEqual(remove_user_from_step_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
