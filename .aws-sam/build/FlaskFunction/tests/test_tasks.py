import unittest
from flask import json
from app import app

class TestTaskManagement(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Test Task',
            'description': 'This is a test task.',
            'assigned_to': 'user_id_123',
            'due_date': '2023-12-31'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('task_id', response.get_json())

    def test_get_tasks(self):
        response = self.app.get('/tasks/me')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Task to Update',
            'description': 'This task will be updated.',
            'assigned_to': 'user_id_123',
            'due_date': '2023-12-31'
        })
        task_id = response.get_json()['task_id']
        
        update_response = self.app.put(f'/tasks/{task_id}', json={
            'status': 'Completed'
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.get_json()['status'], 'Completed')

    def test_delete_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Task to Delete',
            'description': 'This task will be deleted.',
            'assigned_to': 'user_id_123',
            'due_date': '2023-12-31'
        })
        task_id = response.get_json()['task_id']
        
        delete_response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(delete_response.status_code, 204)

if __name__ == '__main__':
    unittest.main()