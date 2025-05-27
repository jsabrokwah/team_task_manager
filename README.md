# Task Management System

A serverless task management application built with AWS services including Lambda, DynamoDB, S3, and SNS.

## Architecture

- **Frontend**: Static website hosted on S3
- **Backend**: Flask application running on AWS Lambda
- **Database**: DynamoDB for storing users and tasks
- **Notifications**: SNS for task notifications
- **Scheduled Events**: CloudWatch Events for daily task reminders

## Deployment Instructions

### Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.12

### Deployment Steps

1. Clone the repository
2. Navigate to the project root directory
3. Build the SAM application:
   ```
   sam build
   ```
4. Deploy the application:
   ```
   sam deploy --guided
   ```
5. During the guided deployment, you will be prompted for:
   - Stack name
   - AWS Region
   - JWT Secret Key (for authentication)
   - Confirmation of IAM role creation

### Environment Variables

The following environment variables are used in the application:

- `USERS_TABLE`: DynamoDB table for user data
- `TASKS_TABLE`: DynamoDB table for task data
- `TASK_NOTIFICATION_TOPIC`: SNS topic ARN for notifications
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `JWT_ACCESS_TOKEN_EXPIRES`: Access token expiration time in seconds
- `JWT_REFRESH_TOKEN_EXPIRES`: Refresh token expiration time in seconds

## Testing

Run the tests using pytest:

```
cd flask-backend
pytest
```

## Frontend Setup

After deployment, update the `config.js` file in the `static-site/js` directory with the API endpoint URL from the CloudFormation outputs.