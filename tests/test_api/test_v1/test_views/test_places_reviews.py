#!/usr/bin/python3
"""test places reviews"""

import unittest
import json
from api.v1.app import app
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

class TestReview(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user = User(email="test@example.com", password="password")
        storage.new(self.user)
        storage.save()
        self.place = Place(name="Test Place", user_id=self.user.id)
        storage.new(self.place)
        storage.save()
        self.review = Review(text="Test Review", place_id=self.place.id, user_id=self.user.id)
        storage.new(self.review)
        storage.save()

    def tearDown(self):
        storage.delete(self.review)
        storage.delete(self.place)
        storage.delete(self.user)
        storage.save()

    def test_get_reviews(self):
        response = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)

    def test_get_review(self):
        response = self.client.get(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_review(self):
        response = self.client.post(f'/api/v1/places/{self.place.id}/reviews', json={'text': 'New Review', 'user_id': self.user.id})
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_json(self):
        response = self.client.post(f'/api/v1/places/{self.place.id}/reviews', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_user_id(self):
        response = self.client.post(f'/api/v1/places/{self.place.id}/reviews', json={'text': 'New Review'})
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_text(self):
        response = self.client.post(f'/api/v1/places/{self.place.id}/reviews', json={'user_id': self.user.id})
        self.assertEqual(response.status_code, 400)

    def test_update_review(self):
        response = self.client.put(f'/api/v1/reviews/{self.review.id}', json={'text': 'Updated Review'})
        self.assertEqual(response.status_code, 200)

    def test_update_review_invalid_json(self):
        response = self.client.put(f'/api/v1/reviews/{self.review.id}', data='Invalid JSON', content_type='text/plain')
        self.assertEqual(response.status_code, 400)

    def test_update_review_not_found(self):
        response = self.client.put('/api/v1/reviews/invalid_id', json={'text': 'Updated Review'})
        self.assertEqual(response.status_code, 404)

    def test_delete_review(self):
        response = self.client.delete(f'/api/v1/reviews/{self.review.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
