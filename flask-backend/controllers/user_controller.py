from flask import Blueprint, request, jsonify
from models.user_model import User
from services.auth_service import AuthService
from utils.validation import validate_user_data

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    if not validate_user_data(data):
        return jsonify({"error": "Invalid user data"}), 400

    user = User(**data)
    user.save()
    return jsonify({"message": "User created successfully", "user_id": user.user_id}), 201

@user_controller.route('/user/update/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.update(**data)
    return jsonify({"message": "User updated successfully"}), 200

@user_controller.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200

@user_controller.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

@user_controller.route('/user/all', methods=['GET'])
def get_all_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200
