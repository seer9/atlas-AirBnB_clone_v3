#!/usr/bin/python3
"""test users"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.user import User

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User(email="test@example.com", password="password")
        storage.new(self.user)
        storage.save()

    def tearDown(self):
        storage.delete(self.user)
        storage.save()

    def test_get_users(self):
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        response = self.client.get(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        response = self.client.post('/api/v1/users', json={'email': 'new@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_json(self):
        response = self.client.post('/api/v1/users', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_email(self):
        response = self.client.post('/api/v1/users', json={'password': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_password(self):
        response = self.client.post('/api/v1/users', json={'email': 'new@example.com'})
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        response = self.client.put(f'/api/v1/users/{self.user.id}', json={'first_name': 'Updated'})
        self.assertEqual(response.status_code, 200)

    def test_update_user_invalid_json(self):
        response = self.client.put(f'/api/v1/users/{self.user.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_user_not_found(self):
        response = self.client.put('/api/v1/users/invalid_id', json={'first_name': 'Updated'})
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        response = self.client.delete(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_not_found(self):
        response = self.client.delete('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
