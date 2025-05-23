from flask import json
from flask_testing import TestCase
from app import app

class TestAuth(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_login(self):
        response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_login_invalid(self):
        response = self.client.post('/login', json={
            'email': 'invalid@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('message', response.json)

    def test_refresh_token(self):
        login_response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        access_token = login_response.json['access_token']
        response = self.client.post('/refresh', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_logout(self):
        login_response = self.client.post('/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        access_token = login_response.json['access_token']
        response = self.client.post('/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)