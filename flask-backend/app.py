from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from controllers.auth_controller import AuthController
from controllers.task_controller import TaskController
from controllers.user_controller import UserController

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize controllers
auth_controller = AuthController()
task_controller = TaskController()
user_controller = UserController()

# Set up routes
app.add_url_rule('/login', view_func=auth_controller.login, methods=['POST'])
app.add_url_rule('/logout', view_func=auth_controller.logout, methods=['POST'])
app.add_url_rule('/refresh', view_func=auth_controller.refresh_token, methods=['POST'])

app.add_url_rule('/tasks', view_func=task_controller.create_task, methods=['POST'])
app.add_url_rule('/tasks/<task_id>', view_func=task_controller.update_task, methods=['PUT'])
app.add_url_rule('/tasks/<task_id>', view_func=task_controller.delete_task, methods=['DELETE'])
app.add_url_rule('/tasks', view_func=task_controller.get_all_tasks, methods=['GET'])
app.add_url_rule('/tasks/me', view_func=task_controller.get_user_tasks, methods=['GET'])

app.add_url_rule('/user/create', view_func=user_controller.create_user, methods=['POST'])
app.add_url_rule('/user/update/<user_id>', view_func=user_controller.update_user, methods=['PUT'])
app.add_url_rule('/user/delete/<user_id>', view_func=user_controller.delete_user, methods=['DELETE'])
app.add_url_rule('/user/all', view_func=user_controller.get_all_users, methods=['GET'])
app.add_url_rule('/user/<user_id>', view_func=user_controller.get_user, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)