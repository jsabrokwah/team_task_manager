from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
from models.task_model import Task
from services.task_service import TaskService
from utils.validation import validate_task_data


class TaskController(Resource):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.task_service = TaskService(dynamodb)

    def get_task(self, task_id=None):
        if task_id:
            task = self.task_service.get_task(task_id)
            if task:
                return jsonify(task)
            return jsonify({"message": "Task not found"}), 404
        tasks = self.task_service.list_tasks()
        return jsonify(tasks)

    @jwt_required()
    def create_task(self):
        data = request.get_json()
        try:
            validate_task_data(data)
        except Exception as e:
            return jsonify({"message": str(e)}), 400
            
        task = self.task_service.create_task(data)
        return jsonify(task), 201

    @jwt_required()
    def update_task(self, task_id):
        data = request.get_json()
        try:
            validate_task_data(data)
        except Exception as e:
            return jsonify({"message": str(e)}), 400
            
        updated_task = self.task_service.update_task(task_id, data)
        if updated_task:
            return jsonify(updated_task)
        return jsonify({"message": "Task not found"}), 404

    @jwt_required()
    def delete_task(self, task_id):
        success = self.task_service.delete_task(task_id)
        if success:
            return jsonify({"message": "Task deleted successfully"})
        return jsonify({"message": "Task not found"}), 404
        
    @jwt_required()
    def get_all_tasks(self):
        tasks = self.task_service.list_tasks()
        return jsonify(tasks)
    
    @jwt_required()
    def get_user_tasks(self):
        user_id = get_jwt_identity()
        tasks = self.task_service.list_tasks(assigned_to=user_id)
        return jsonify(tasks)
    
    @jwt_required()
    def get_user_tasks_by_status(self, status):
        user_id = get_jwt_identity()
        tasks = self.task_service.list_tasks(assigned_to=user_id, status=status)
        if tasks:
            return jsonify(tasks)
        return jsonify({"message": "No tasks found with the specified status"}), 404
        
    @jwt_required()
    def get_tasks_by_status(self, status):
        tasks = self.task_service.list_tasks(status=status)
        if tasks:
            return jsonify(tasks)
        return jsonify({"message": "No tasks found with the specified status"}), 404