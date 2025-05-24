from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from models.user_model import User
from utils.jwt_helper import create_access_token, verify_access_token

class AuthService:
    def __init__(self, user_model, jwt_helper):
        self.user_model = user_model
        self.jwt_helper = jwt_helper

    def register_user(self, user_data):
        # If user_data does not contain 'user_id', generate one
        if 'user_id' not in user_data:
            user_data['user_id'] = self.user_model.generate_user_id()

        # Check if user already exists
        existing_user = self.user_model.get_user(user_data['user_id'])
        if existing_user:
            return {"message": "User already exists"}, 400
        
        # Hash the password
        user_data['hashed_password'] = generate_password_hash(user_data['password'])
        del user_data['password']  # Remove plain password for security

        # Create user in the database
        success = self.user_model.create_user(user_data)
        if success:
            return {"message": "User registered successfully"}, 201
        return {"message": "Failed to register user"}, 500

    def login(self, email, password):
        # Retrieve user by email
        user = self.user_model.get_user_by_email(email)
        if not user:
            return {"message": "Invalid email or password"}, 401

        # Verify password
        if not check_password_hash(user['hashed_password'], password):
            return {"message": "Invalid email or password"}, 401

        # Generate JWT tokens
        access_token = create_access_token({"user_id": user['user_id']})
        refresh_token = create_access_token({"user_id": user['user_id']}, expires_delta=timedelta(days=1))

        # Update refresh token in the database
        self.user_model.update_user(user['user_id'], {"refresh_token": refresh_token})

        return {"access_token": access_token, "refresh_token": refresh_token}, 200

    def refresh_token(self, refresh_token):
        # Verify the refresh token
        payload = verify_access_token(refresh_token)
        if not payload:
            return {"message": "Invalid refresh token"}, 401

        # Generate a new access token
        access_token = create_access_token({"user_id": payload['user_id']})
        return {"access_token": access_token}, 200

    def logout(self, user_id):
        # Remove refresh token from the database
        success = self.user_model.update_user(user_id, {"refresh_token": None})
        if success:
            return {"message": "Logout successful"}, 200
        return {"message": "Failed to logout"}, 500

    def validate_token(self, token):
        # Verify the token
        payload = verify_access_token(token)
        if not payload:
            return {"message": "Invalid token"}, 401
        return {"message": "Token is valid", "user_id": payload['user_id']}, 200