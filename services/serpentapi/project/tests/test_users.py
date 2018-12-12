# services/users/project/tests/test_users.py


import json
import unittest

from project import db
from project.api.models.user import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users API Endpoint."""

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'monty',
                    'email': 'monty@python.org',
                    'password': 'holygrail'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            print(response.data)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('monty@python.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'monty',
                    'email': 'monty@python.org',
                    'password': 'holygrail'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'monty',
                    'email': 'monty@python.org'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('monty', 'monty@python.org', 'holygrail')
        with self.client:
            response = self.client.get(f'/api/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('monty', data['data']['username'])
            self.assertIn('monty@python.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/api/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/api/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('monty', 'monty@python.org', 'holygrail')
        add_user('fletcher', 'fletcher@notreal.com', 'holygrail')
        with self.client:
            response = self.client.get('/api/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('monty', data['data']['users'][0]['username'])
            self.assertIn(
                'monty@python.org', data['data']['users'][0]['email'])
            self.assertTrue(data['data']['users'][0]['active'])  # new
            self.assertFalse(data['data']['users'][0]['admin'])  # new
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn(
                'fletcher@notreal.com', data['data']['users'][1]['email'])
            self.assertTrue(data['data']['users'][1]['active'])  # new
            self.assertFalse(data['data']['users'][1]['admin'])  # new
            self.assertIn('success', data['status'])

    # def test_main_no_users(self):
    #     """Ensure the main route behaves correctly when no users have been
    #     added to the database."""
    #     response = self.client.get('/api/users')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'All Users', response.data)
    #     self.assertIn(b'<p>No users!</p>', response.data)

    # def test_main_with_users(self):
    #     """Ensure the main route behaves correctly when users have been
    #     added to the database."""
    #     add_user('monty', 'monty@python.org', 'holygrail')
    #     add_user('fletcher', 'fletcher@notreal.com', 'holygrail')
    #     with self.client:
    #         response = self.client.get('/api/users')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'All Users', response.data)
    #         self.assertNotIn(b'<p>No users!</p>', response.data)
    #         self.assertIn(b'monty', response.data)
    #         self.assertIn(b'fletcher', response.data)

    # def test_main_add_user(self):
    #     """Ensure a new user can be added to the database."""
    #     with self.client:
    #         response = self.client.post(
    #             '/api/users/add',
    #             data=dict(
    #                 username='monty',
    #                 email='monty@sonotreal.com',
    #                 password='holygrail'
    #             ),
    #             follow_redirects=True
    #         )
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'All Users', response.data)
    #         self.assertNotIn(b'<p>No users!</p>', response.data)
    #         self.assertIn(b'monty', response.data)

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps(dict(
                    username='monty',
                    email='monty@reallynotreal.com')),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'monty',
                    'email': 'monty@sonotreal.com',
                    'password': 'test'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_add_user_not_admin(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'monty',
                    'email': 'monty@sonotreal.com',
                    'password': 'test'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
