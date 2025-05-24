import pytest
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/user/create', json={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'user_id' in data

def test_get_user(client):
    response = client.get('/user/1')  # Assuming user with ID 1 exists
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test User'

def test_update_user(client):
    response = client.put('/user/update/1', json={
        'name': 'Updated User'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Updated User'

def test_delete_user(client):
    response = client.delete('/user/delete/1')  # Assuming user with ID 1 exists
    assert response.status_code == 204

def test_get_all_users(client):
    response = client.get('/user/all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Should return a list of users