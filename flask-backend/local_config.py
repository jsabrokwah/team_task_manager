import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Override DynamoDB settings for local development
os.environ['AWS_REGION'] = 'localhost'
os.environ['DYNAMODB_ENDPOINT'] = 'http://localhost:8000'
os.environ['AWS_ACCESS_KEY_ID'] = 'dummy'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'

# Use local tables
os.environ['USERS_TABLE'] = 'Users'
os.environ['TASKS_TABLE'] = 'Tasks'

# Mock SNS topic
os.environ['TASK_NOTIFICATION_TOPIC'] = 'arn:aws:sns:us-east-1:123456789012:TaskNotifications'
