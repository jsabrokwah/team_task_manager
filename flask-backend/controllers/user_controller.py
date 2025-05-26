from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import User
from services.auth_service import AuthService
from utils.validation import validate_user_data

user_controller = Blueprint('user_controller', __name__)

@jwt_required()
def create_user():
    # Check if current user is admin
    current_user_id = get_jwt_identity()
    current_user = User.get_user(current_user_id)
    if not current_user or current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
    data = request.get_json()
    try:
        validate_user_data(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    success = User.create_user(data)
    if success:
        return jsonify({"message": "User created successfully", "user_id": data.get('user_id')}), 201
    return jsonify({"error": "Failed to create user"}), 500

@jwt_required()
def update_user(user_id):
    # Check if current user is admin or the user being updated
    current_user_id = get_jwt_identity()
    current_user = User.get_user(current_user_id)
    if not current_user or (current_user.get('role') != 'admin' and current_user_id != user_id):
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.get_json()
    
    # Don't allow role change unless admin
    if 'role' in data and current_user.get('role') != 'admin':
        return jsonify({"error": "Cannot change role. Admin access required"}), 403
    
    success = User.update_user(user_id, data)
    if success:
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found or update failed"}), 404

@jwt_required()
def delete_user(user_id):
    # Check if current user is admin
    current_user_id = get_jwt_identity()
    current_user = User.get_user(current_user_id)
    if not current_user or current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
    success = User.delete_user(user_id)
    if success:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@jwt_required()
def get_user(user_id):
    # Check if current user is admin or the requested user
    current_user_id = get_jwt_identity()
    current_user = User.get_user(current_user_id)
    if not current_user or (current_user.get('role') != 'admin' and current_user_id != user_id):
        return jsonify({"error": "Unauthorized"}), 403
        
    user = User.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Remove sensitive information
    if 'hashed_password' in user:
        del user['hashed_password']
    if 'refresh_token' in user:
        del user['refresh_token']
        
    return jsonify(user), 200

@jwt_required()
def get_all_users():
    # Check if current user is admin
    current_user_id = get_jwt_identity()
    current_user = User.get_user(current_user_id)
    if not current_user or current_user.get('role') != 'admin':
        return jsonify({"error": "Unauthorized. Admin access required"}), 403
        
    users = User.get_all_users()
    
    # Remove sensitive information
    for user in users:
        if 'hashed_password' in user:
            del user['hashed_password']
        if 'refresh_token' in user:
            del user['refresh_token']
            
    return jsonify(users), 200
