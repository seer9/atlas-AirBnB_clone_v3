#!/usr/bin/python3
"""test cities"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.state import State
from models.city import City

class TestCity(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.state = State(name="Test State")
        storage.new(self.state)
        storage.save()
        self.city = City(name="Test City", state_id=self.state.id)
        storage.new(self.city)
        storage.save()

    def tearDown(self):
        storage.delete(self.city)
        storage.delete(self.state)
        storage.save()

    def test_get_cities(self):
        response = self.client.get(f'/api/v1/states/{self.state.id}/cities')
        self.assertEqual(response.status_code, 200)

    def test_get_city(self):
        response = self.client.get(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_city_not_found(self):
        response = self.client.get('/api/v1/cities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_city(self):
        response = self.client.post(f'/api/v1/states/{self.state.id}/cities', json={'name': 'New City'})
        self.assertEqual(response.status_code, 201)

    def test_create_city_invalid_json(self):
        response = self.client.post(f'/api/v1/states/{self.state.id}/cities', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_city_missing_name(self):
        response = self.client.post(f'/api/v1/states/{self.state.id}/cities', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_city(self):
        response = self.client.put(f'/api/v1/cities/{self.city.id}', json={'name': 'Updated City'})
        self.assertEqual(response.status_code, 200)

    def test_update_city_invalid_json(self):
        response = self.client.put(f'/api/v1/cities/{self.city.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_city_not_found(self):
        response = self.client.put('/api/v1/cities/invalid_id', json={'name': 'Updated City'})
        self.assertEqual(response.status_code, 404)

    def test_delete_city(self):
        response = self.client.delete(f'/api/v1/cities/{self.city.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_city_not_found(self):
        response = self.client.delete('/api/v1/cities/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
