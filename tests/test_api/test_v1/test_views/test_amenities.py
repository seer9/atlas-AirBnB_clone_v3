#!/usr/bin/python3
"""test amenities"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.amenity = Amenity(name="Test Amenity")
        storage.new(self.amenity)
        storage.save()

    def tearDown(self):
        storage.delete(self.amenity)
        storage.save()

    def test_get_amenities(self):
        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity(self):
        response = self.client.get(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities', json={'name': 'New Amenity'})
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid_json(self):
        response = self.client.post('/api/v1/amenities', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities', json={})
        self.assertEqual(response.status_code, 400)

    def test_update_amenity(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity.id}', json={'name': 'Updated Amenity'})
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_invalid_json(self):
        response = self.client.put(f'/api/v1/amenities/{self.amenity.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_not_found(self):
        response = self.client.put('/api/v1/amenities/invalid_id', json={'name': 'Updated Amenity'})
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        response = self.client.delete(f'/api/v1/amenities/{self.amenity.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_amenity_not_found(self):
        response = self.client.delete('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
