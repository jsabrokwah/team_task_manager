from flask import request
from dateutil.parser import parse
from werkzeug.exceptions import BadRequest

def validate_user_data(user_data):
    if not isinstance(user_data, dict):
        raise BadRequest("User data must be a JSON object.")
    
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in user_data:
            raise BadRequest(f"Missing required field: {field}")
    
    if not isinstance(user_data['name'], str) or len(user_data['name']) < 1:
        raise BadRequest("Name must be a non-empty string.")
    
    if not isinstance(user_data['email'], str) or '@' not in user_data['email']:
        raise BadRequest("Email must be a valid email address.")
    
    if not isinstance(user_data['password'], str) or len(user_data['password']) < 6:
        raise BadRequest("Password must be at least 6 characters long.")

def validate_task_data(task_data):
    if not isinstance(task_data, dict):
        raise BadRequest("Task data must be a JSON object.")
    
    required_fields = ['title', 'description', 'assigned_to', 'due_date']
    for field in required_fields:
        if field not in task_data:
            raise BadRequest(f"Missing required field: {field}")
    
    if not isinstance(task_data['title'], str) or len(task_data['title']) < 1:
        raise BadRequest("Title must be a non-empty string.")
    
    if not isinstance(task_data['description'], str):
        raise BadRequest("Description must be a string.")
    
    if not isinstance(task_data['assigned_to'], str) or len(task_data['assigned_to']) < 1:
        raise BadRequest("Assigned_to must be a non-empty string.")
    
    if not isinstance(task_data['due_date'], str):
        raise BadRequest("Due_date must be a string in ISO format.")

def validate_login(login_data):
    if not isinstance(login_data, dict):
        raise BadRequest("Login data must be a JSON object.")
    
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in login_data:
            raise BadRequest(f"Missing required field: {field}")
    
    if not isinstance(login_data['email'], str) or '@' not in login_data['email']:
        raise BadRequest("Email must be a valid email address.")
    
    if not isinstance(login_data['password'], str) or len(login_data['password']) < 6:
        raise BadRequest("Password must be at least 6 characters long.")


def validate_registration(registration_data):
    if not isinstance(registration_data, dict):
        raise BadRequest("Registration data must be a JSON object.")
    
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in registration_data:
            raise BadRequest(f"Missing required field: {field}")
    
    if not isinstance(registration_data['name'], str) or len(registration_data['name']) < 1:
        raise BadRequest("Name must be a non-empty string.")
    
    if not isinstance(registration_data['email'], str) or '@' not in registration_data['email']:
        raise BadRequest("Email must be a valid email address.")
    
    if not isinstance(registration_data['password'], str) or len(registration_data['password']) < 6:
        raise BadRequest("Password must be at least 6 characters long.")
    