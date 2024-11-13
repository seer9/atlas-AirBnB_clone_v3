#!/usr/bin/python3
"""test states"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State

class TestState(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.state = State(name="Test State")
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        storage.delete(self.state)
        storage.save()

    def test_get_states(self):
        response = self.client.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)

    def test_get_state(self):
        response = self.client.get(f'/api/v1/states/{self.state.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_state_not_found(self):
        response = self.client.get('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        response = self.client.post('/api/v1/states', json={'name': 'New State'})
        self.assertEqual(response.status_code, 201)

    def test_create_state_invalid_json(self):
        response = self.client.post('/api/v1/states', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_state_missing_name(self):
        response = self.client.post('/api/v1/states', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        response = self.client.put(f'/api/v1/states/{self.state.id}', json={'name': 'Updated State'})
        self.assertEqual(response.status_code, 200)

    def test_update_state_invalid_json(self):
        response = self.client.put(f'/api/v1/states/{self.state.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_state_not_found(self):
        response = self.client.put('/api/v1/states/invalid_id', json={'name': 'Updated State'})
        self.assertEqual(response.status_code, 404)

    def test_delete_state(self):
        response = self.client.delete(f'/api/v1/states/{self.state.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_state_not_found(self):
        response = self.client.delete('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
