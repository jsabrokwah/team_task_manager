import pytest
import os
import boto3
from moto import mock_dynamodb, mock_sns
from app import app as flask_app

@pytest.fixture
def app():
    # Set test environment variables
    os.environ['USERS_TABLE'] = 'Users-Test'
    os.environ['TASKS_TABLE'] = 'Tasks-Test'
    os.environ['TASK_NOTIFICATION_TOPIC'] = 'arn:aws:sns:us-east-1:123456789012:TaskNotifications-Test'
    os.environ['JWT_SECRET_KEY'] = 'test_secret_key'
    os.environ['JWT_ACCESS_TOKEN_EXPIRES'] = '3600'
    os.environ['JWT_REFRESH_TOKEN_EXPIRES'] = '86400'
    
    # Configure app for testing
    flask_app.config.update({
        'TESTING': True,
    })
    
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    with mock_dynamodb():
        # Create mock DynamoDB tables
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        
        # Create Users table
        dynamodb.create_table(
            TableName='Users-Test',
            KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'user_id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        # Create Tasks table
        dynamodb.create_table(
            TableName='Tasks-Test',
            KeySchema=[{'AttributeName': 'task_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'task_id', 'AttributeType': 'S'},
                {'AttributeName': 'assigned_to', 'AttributeType': 'S'},
                {'AttributeName': 'status', 'AttributeType': 'S'},
                {'AttributeName': 'due_date', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'AssignedToIndex',
                    'KeySchema': [{'AttributeName': 'assigned_to', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                {
                    'IndexName': 'StatusIndex',
                    'KeySchema': [{'AttributeName': 'status', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                {
                    'IndexName': 'DueDateIndex',
                    'KeySchema': [{'AttributeName': 'due_date', 'KeyType': 'HASH'}],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        
        yield dynamodb

@pytest.fixture
def mock_sns():
    with mock_sns():
        sns = boto3.client('sns', region_name='us-east-1')
        # Create a mock SNS topic
        sns.create_topic(Name='TaskNotifications-Test')
        yield sns