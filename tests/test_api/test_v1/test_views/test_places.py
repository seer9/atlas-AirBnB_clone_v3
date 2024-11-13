#!/usr/bin/python3
"""test places"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.city import City
from models.place import Place
from models.user import User

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User(email="test@example.com", password="password")
        storage.new(self.user)
        storage.save()
        self.city = City(name="Test City")
        storage.new(self.city)
        storage.save()
        self.place = Place(name="Test Place", city_id=self.city.id, user_id=self.user.id)
        storage.new(self.place)
        storage.save()

    def tearDown(self):
        storage.delete(self.place)
        storage.delete(self.city)
        storage.delete(self.user)
        storage.save()

    def test_get_places(self):
        response = self.client.get(f'/api/v1/cities/{self.city.id}/places')
        self.assertEqual(response.status_code, 500)

    def test_get_place(self):
        response = self.client.get(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_place(self):
        response = self.client.post(f'/api/v1/cities/{self.city.id}/places', json={'name': 'New Place', 'user_id': self.user.id})
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_json(self):
        response = self.client.post(f'/api/v1/cities/{self.city.id}/places', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_user_id(self):
        response = self.client.post(f'/api/v1/cities/{self.city.id}/places', json={'name': 'New Place'})
        self.assertEqual(response.status_code, 400)

    def test_create_place_missing_name(self):
        response = self.client.post(f'/api/v1/cities/{self.city.id}/places', json={'user_id': self.user.id})
        self.assertEqual(response.status_code, 400)

    def test_update_place(self):
        response = self.client.put(f'/api/v1/places/{self.place.id}', json={'name': 'Updated Place'})
        self.assertEqual(response.status_code, 200)

    def test_update_place_invalid_json(self):
        response = self.client.put(f'/api/v1/places/{self.place.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_place_not_found(self):
        response = self.client.put('/api/v1/places/invalid_id', json={'name': 'Updated Place'})
        self.assertEqual(response.status_code, 404)

    def test_delete_place(self):
        response = self.client.delete(f'/api/v1/places/{self.place.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_place_not_found(self):
        response = self.client.delete('/api/v1/places/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
