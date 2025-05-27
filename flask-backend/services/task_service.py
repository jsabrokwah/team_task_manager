from datetime import datetime, timezone
import uuid
import boto3
import os
import logging
from botocore.exceptions import ClientError
from services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class TaskService:
    def __init__(self, dynamodb_resource):
        self.dynamodb = dynamodb_resource
        try:
            tasks_table_name = os.environ.get('TASKS_TABLE', 'Tasks')
            self.tasks_table = self.dynamodb.Table(tasks_table_name)
            self.notification_service = NotificationService()
        except Exception as e:
            logger.error(f"Error initializing TaskService: {str(e)}")
            raise

    def create_task(self, task_data):
        # Generate task_id if not provided
        if 'task_id' not in task_data:
            task_data['task_id'] = f"task_{uuid.uuid4().hex}"
            
        # Set default status if not provided
        if 'status' not in task_data:
            task_data['status'] = 'Pending'

        item = {
            'task_id': task_data['task_id'],
            'assigned_to': task_data['assigned_to'],
            'title': task_data['title'],
            'description': task_data['description'],
            'status': task_data['status'],
            'due_date': task_data['due_date'],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }

        try:
            self.tasks_table.put_item(Item=item)
            # Send notification for task assignment
            self.notification_service.send_task_assignment_notification(item)
            return item
        except ClientError as e:
            logger.error(f"Error creating task: {str(e)}")
            return None

    def get_task(self, task_id):
        try:
            response = self.tasks_table.get_item(Key={'task_id': task_id})
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Error getting task: {str(e)}")
            return None

    def update_task(self, task_id, updates):
        update_expression = "SET "
        expression_attribute_values = {}
        
        for key, value in updates.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(", ")
        update_expression += ", updated_at = :updated_at"
        expression_attribute_values[":updated_at"] = datetime.now(timezone.utc).isoformat()

        try:
            response = self.tasks_table.update_item(
                Key={'task_id': task_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            updated_task = response.get('Attributes')
            
            # Send notification for status update if status was changed
            if 'status' in updates:
                self.notification_service.send_task_status_notification(updated_task)
                
            return updated_task
        except ClientError as e:
            logger.error(f"Error updating task: {str(e)}")
            return None

    def delete_task(self, task_id):
        try:
            task = self.get_task(task_id)
            if not task:
                return False
                
            self.tasks_table.delete_item(Key={'task_id': task_id})
            return True
        except ClientError as e:
            logger.error(f"Error deleting task: {str(e)}")
            return False

    def list_tasks(self, assigned_to=None, status=None):
        filter_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        if assigned_to:
            filter_expression.append("#assigned_to = :assigned_to")
            expression_attribute_values[":assigned_to"] = assigned_to
            expression_attribute_names["#assigned_to"] = "assigned_to"

        if status:
            filter_expression.append("#status = :status")
            expression_attribute_values[":status"] = status
            expression_attribute_names["#status"] = "status"

        try:
            scan_kwargs = {}
            if filter_expression:
                scan_kwargs['FilterExpression'] = " AND ".join(filter_expression)
                scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values
                scan_kwargs['ExpressionAttributeNames'] = expression_attribute_names

            response = self.tasks_table.scan(**scan_kwargs)
            items = response.get('Items', [])
            
            # Handle pagination for large result sets
            while 'LastEvaluatedKey' in response:
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = self.tasks_table.scan(**scan_kwargs)
                items.extend(response.get('Items', []))
                
            return items
        except ClientError as e:
            logger.error(f"Error listing tasks: {str(e)}")
            return []