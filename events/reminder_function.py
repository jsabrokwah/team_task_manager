import boto3
import json
import logging
from datetime import datetime, timedelta, timezone
import os
from botocore.exceptions import ClientError
from dateutil import parser

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function to send reminders for tasks due within the next 24 hours.
    """
    # Initialize DynamoDB and SNS clients
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')

    # Get environment variables with defaults
    tasks_table_name = os.environ.get('TASKS_TABLE', 'Tasks')
    topic_arn = os.environ.get('TASK_NOTIFICATION_TOPIC')
    
    if not topic_arn:
        logger.error("TASK_NOTIFICATION_TOPIC environment variable not set")
        return {
            'statusCode': 500,
            'body': 'Missing required environment variable: TASK_NOTIFICATION_TOPIC'
        }

    # Get the Tasks table
    try:
        tasks_table = dynamodb.Table(tasks_table_name)
    except Exception as e:
        logger.error(f"Error accessing DynamoDB table {tasks_table_name}: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Failed to access DynamoDB table: {str(e)}'
        }

    # Get today's date and calculate the reminder date range (next 24 hours)
    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(days=1)
    
    # Format dates for comparison
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    
    logger.info(f"Checking for tasks due on {tomorrow_str}")

    # Scan the Tasks table for tasks due tomorrow
    try:
        tasks_to_remind = []
        response = tasks_table.scan()
        items = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = tasks_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        # Filter tasks due tomorrow
        for task in items:
            if 'due_date' in task:
                try:
                    # Parse the due date string to a datetime object
                    due_date = parser.parse(task['due_date']).date()
                    task_due_date_str = due_date.strftime('%Y-%m-%d')
                    
                    # Check if the task is due tomorrow
                    if task_due_date_str == tomorrow_str:
                        tasks_to_remind.append(task)
                except Exception as e:
                    logger.warning(f"Error parsing due date for task {task.get('task_id')}: {str(e)}")
        
        logger.info(f"Found {len(tasks_to_remind)} tasks due tomorrow")
        
        # Send reminders for tasks due tomorrow
        reminders_sent = 0
        for task in tasks_to_remind:
            try:
                # Get user details to personalize the message
                user_id = task.get('assigned_to')
                user_table = dynamodb.Table('Users')
                user_response = user_table.get_item(Key={'user_id': user_id})
                user = user_response.get('Item', {})
                user_name = user.get('name', 'Team Member')
                
                # Create a detailed message
                message = {
                    "type": "TASK_REMINDER",
                    "task_id": task['task_id'],
                    "title": task['title'],
                    "description": task.get('description', ''),
                    "due_date": task['due_date'],
                    "user_name": user_name,
                    "user_id": user_id
                }
                
                # Send the reminder
                sns.publish(
                    TopicArn=topic_arn,
                    Message=json.dumps(message),
                    Subject=f"Reminder: Task '{task['title']}' is due tomorrow"
                )
                reminders_sent += 1
            except ClientError as e:
                logger.error(f"Error sending reminder for task {task.get('task_id')}: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error sending reminder: {str(e)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Reminders processed successfully',
                'tasks_found': len(tasks_to_remind),
                'reminders_sent': reminders_sent
            })
        }
    except ClientError as e:
        logger.error(f"DynamoDB error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'DynamoDB error: {str(e)}'})
        }
    except Exception as e:
        logger.error(f"Error processing reminders: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error processing reminders: {str(e)}'})
        }