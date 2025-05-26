import boto3
import os
import json
from botocore.exceptions import ClientError

class NotificationService:
    def __init__(self):
        self.sns = boto3.client('sns')
        self.topic_arn = os.environ.get('TASK_NOTIFICATION_TOPIC', 'default_topic_arn')
        
    def send_task_assignment_notification(self, task):
        """Send notification when a task is assigned to a user"""
        try:
            message = {
                "type": "TASK_ASSIGNED",
                "task_id": task['task_id'],
                "title": task['title'],
                "assigned_to": task['assigned_to'],
                "due_date": task['due_date']
            }
            
            self.sns.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(message),
                Subject=f"New Task Assigned: {task['title']}"
            )
            return True
        except ClientError as e:
            print(f"Error sending task assignment notification: {str(e)}")
            return False
            
    def send_task_status_notification(self, task):
        """Send notification when a task status is updated"""
        try:
            message = {
                "type": "TASK_STATUS_UPDATED",
                "task_id": task['task_id'],
                "title": task['title'],
                "status": task['status'],
                "assigned_to": task['assigned_to']
            }
            
            self.sns.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(message),
                Subject=f"Task Status Updated: {task['title']}"
            )
            return True
        except ClientError as e:
            print(f"Error sending task status notification: {str(e)}")
            return False