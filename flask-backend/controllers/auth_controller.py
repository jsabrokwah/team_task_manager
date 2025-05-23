from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity
from services.auth_service import AuthService
from utils.validation import validate_login, validate_registration

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = validate_login(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = auth_service.authenticate(data['email'], data['password'])
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user['user_id'])
    refresh_token = create_refresh_token(identity=user['user_id'])
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    # Implement logout logic if needed (e.g., blacklist the token)
    return jsonify({"msg": "Logout successful"}), 200