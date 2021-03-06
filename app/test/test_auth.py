import unittest
import json
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


class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
        user_response = register_user(self)
        response_data = json.loads(user_response.data)
        self.assertTrue(response_data.get('Authorization'))
        self.assertEqual(user_response.status_code, 201)

        login_response = login_user(self)
        data = json.loads(login_response.data)
        self.assertTrue(data.get('Authorization'))
        self.assertEqual(login_response.status_code, 200)

    def test_valid_logout(self):
        with self.client:
            user_response = register_user(self)
            response_data = json.loads(user_response.data)
            self.assertTrue(response_data.get('Authorization'))
            self.assertEqual(user_response.status_code, 201)

            # registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data)
            self.assertTrue(data.get('Authorization'))
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization=json.loads(
                        login_response.data
                    )['Authorization']
                )
            )
            data = json.loads(response.data)
            self.assertTrue(data.get('status') == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
