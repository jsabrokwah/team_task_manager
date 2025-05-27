#!/bin/bash

# Local setup script for Task Management System

echo "Setting up local development environment for Task Management System..."

# Create local DynamoDB tables using AWS CLI
echo "Creating local DynamoDB tables..."

# Check if DynamoDB Local is running
if ! curl -s http://localhost:8000 > /dev/null; then
  echo "Error: DynamoDB Local is not running. Please start it first."
  echo "You can download it from: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html"
  echo "Start it with: java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb"
  exit 1
fi

# Delete existing tables
aws dynamodb delete-table --table-name Users --endpoint-url http://localhost:8000
# Create Users table
aws dynamodb create-table \
  --table-name Users \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --endpoint-url http://localhost:8000

# Delete existing tables
aws dynamodb delete-table --table-name Tasks --endpoint-url http://localhost:8000
# Create Tasks table with GSIs
aws dynamodb create-table \
  --table-name Tasks \
  --attribute-definitions \
    AttributeName=task_id,AttributeType=S \
    AttributeName=assigned_to,AttributeType=S \
    AttributeName=status,AttributeType=S \
    AttributeName=due_date,AttributeType=S \
  --key-schema AttributeName=task_id,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --global-secondary-indexes \
    "[
      {
        \"IndexName\": \"AssignedToIndex\",
        \"KeySchema\": [{\"AttributeName\":\"assigned_to\",\"KeyType\":\"HASH\"}],
        \"Projection\":{\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\":{\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
      },
      {
        \"IndexName\": \"StatusIndex\",
        \"KeySchema\": [{\"AttributeName\":\"status\",\"KeyType\":\"HASH\"}],
        \"Projection\":{\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\":{\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
      },
      {
        \"IndexName\": \"DueDateIndex\",
        \"KeySchema\": [{\"AttributeName\":\"due_date\",\"KeyType\":\"HASH\"}],
        \"Projection\":{\"ProjectionType\":\"ALL\"},
        \"ProvisionedThroughput\":{\"ReadCapacityUnits\":5,\"WriteCapacityUnits\":5}
      }
    ]" \
  --endpoint-url http://localhost:8000

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd flask-backend
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt

# Create a local config file for development
echo "Creating local config file..."
cat > local_config.py << EOL
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
EOL

echo "Setup complete!"
echo ""
echo "To run the Flask application locally:"
echo "1. Make sure DynamoDB Local is running"
echo "2. Activate the virtual environment: source flask-backend/venv/bin/activate"
echo "3. Run the Flask app: cd flask-backend && FLASK_APP=app.py FLASK_ENV=development python -m flask run"
echo ""
echo "To run the frontend locally:"
echo "1. Update static-site/js/config.js with the local API endpoint (http://127.0.0.1:5000/)"
echo "2. Open static-site/index.html in your browser or use a local web server"