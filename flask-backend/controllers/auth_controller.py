from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import User
from utils import jwt_helper
from services.auth_service import AuthService
from utils.validation import validate_login, validate_registration


auth_bp = Blueprint('auth', __name__)
auth_service = AuthService(User, jwt_helper)

def login():
    data = request.get_json()
    try:
        validate_login(data)
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

    result, status_code = auth_service.login(data['email'], data['password'])
    return jsonify(result), status_code

@jwt_required()
def refresh_token():
    current_user = get_jwt_identity()
    result, status_code = auth_service.refresh_token(current_user)
    return jsonify(result), status_code

@jwt_required()
def logout():
    current_user = get_jwt_identity()
    result, status_code = auth_service.logout(current_user)
    return jsonify(result), status_code