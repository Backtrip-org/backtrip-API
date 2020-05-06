import json
import unittest

from app.main.service.chat_message_service import save_message, get_messages
from app.test.base import BaseTestCase
from app.test.test_auth import register_user, login_user
from app.test.test_chat_message_service import get_chat_message_object


class MyTestCase(BaseTestCase):
    def test_get_messages_should_return_ok(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        user_id = json.loads(login_response.data)['id']
        save_message(get_chat_message_object("message", trip_id, user_id))
        get_messages_response = self.client.get('/chat_message/{}'.format(str(trip_id)), headers=headers)
        self.assertEqual(get_messages_response.status_code, 200)

    def test_get_messages_should_return_not_found(self):
        register_user(self)
        login_response = login_user(self)
        headers = dict(Authorization=json.loads(login_response.data)['Authorization'])
        payload = json.dumps(dict(name='trip', picture_path='picture/path'))
        create_trip_response = \
            self.client.post('/trip/', headers=headers, data=payload, content_type='application/json')
        trip_id = json.loads(create_trip_response.data)['id']
        user_id = json.loads(login_response.data)['id']
        save_message(get_chat_message_object("message", trip_id, user_id))
        get_messages_response = self.client.get('/chat_message/{}'.format(str(2)), headers=headers)
        self.assertEqual(get_messages_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
