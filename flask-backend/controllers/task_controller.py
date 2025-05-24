from flask import request, jsonify
from flask_restful import Resource
import boto3
from models.task_model import TaskModel
from services.task_service import TaskService
from utils.validation import validate_task_data

class TaskController(Resource):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.task_service = TaskService(dynamodb)

    def get(self, task_id=None):
        if task_id:
            task = self.task_service.get_task(task_id)
            if task:
                return jsonify(task)
            return jsonify({"message": "Task not found"}), 404
        tasks = self.task_service.get_all_tasks()
        return jsonify(tasks)

    def post(self):
        data = request.get_json()
        if not validate_task_data(data):
            return jsonify({"message": "Invalid task data"}), 400
        task = self.task_service.create_task(data)
        return jsonify(task), 201

    def put(self, task_id):
        data = request.get_json()
        if not validate_task_data(data):
            return jsonify({"message": "Invalid task data"}), 400
        updated_task = self.task_service.update_task(task_id, data)
        if updated_task:
            return jsonify(updated_task)
        return jsonify({"message": "Task not found"}), 404

    def delete(self, task_id):
        success = self.task_service.delete_task(task_id)
        if success:
            return jsonify({"message": "Task deleted successfully"})
        return jsonify({"message": "Task not found"}), 404
    