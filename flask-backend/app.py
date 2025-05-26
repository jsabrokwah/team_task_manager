from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import awsgi
import logging
from controllers.auth_controller import login, logout, refresh_token
from controllers.task_controller import TaskController
from controllers.user_controller import create_user, update_user, delete_user, get_all_users, get_user

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'default_secret_key_for_development')
if app.config['JWT_SECRET_KEY'] == 'default_secret_key_for_development':
    logger.warning("Using default JWT secret key. Set JWT_SECRET_KEY environment variable in production.")
    
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour default
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 604800))  # 1 week default

jwt = JWTManager(app)

# Initialize controllers
task_controller = TaskController()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# Set up routes
# Auth routes
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/logout', view_func=logout, methods=['POST'])
app.add_url_rule('/refresh', view_func=refresh_token, methods=['POST'])

# Task routes
app.add_url_rule('/tasks', view_func=task_controller.create_task, methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=task_controller.update_task, methods=['PUT'])
app.add_url_rule('/tasks/<task_id>', view_func=task_controller.delete_task, methods=['DELETE'])
app.add_url_rule('/tasks', view_func=task_controller.get_all_tasks, methods=['GET'])
app.add_url_rule('/tasks/me', view_func=task_controller.get_user_tasks, methods=['GET'])
app.add_url_rule('/tasks/status/<status>', view_func=task_controller.get_tasks_by_status, methods=['GET'])
app.add_url_rule('/tasks/me/status/<status>', view_func=task_controller.get_user_tasks_by_status, methods=['GET'])

# User routes
app.add_url_rule('/user/create', view_func=create_user, methods=['POST'])
app.add_url_rule('/user/update/<user_id>', view_func=update_user, methods=['PUT'])
app.add_url_rule('/user/delete/<user_id>', view_func=delete_user, methods=['DELETE'])
app.add_url_rule('/user/all', view_func=get_all_users, methods=['GET'])
app.add_url_rule('/user/<user_id>', view_func=get_user, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)

# For AWS Lambda compatibility
def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})