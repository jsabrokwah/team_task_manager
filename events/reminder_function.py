def lambda_handler(event, context):
    import boto3
    from datetime import datetime, timedelta
    import os

    # Initialize DynamoDB and SNS clients
    dynamodb = boto3.resource('dynamodb')
    sns = boto3.client('sns')

    # Get the Tasks table
    tasks_table = dynamodb.Table(os.environ['TASKS_TABLE'])
    
    # Get today's date and calculate the reminder date (24 hours from now)
    today = datetime.now(datetime.timezone.utc)
    reminder_date = today + timedelta(days=1)

    # Scan the Tasks table for tasks due tomorrow
    response = tasks_table.scan(
        FilterExpression='due_date = :due_date',
        ExpressionAttributeValues={
            ':due_date': reminder_date.strftime('%Y-%m-%d')
        }
    )

    # Iterate through the tasks and send reminders
    for task in response['Items']:
        message = f"Reminder: Task '{task['title']}' is due tomorrow."
        sns.publish(
            TopicArn=os.environ['TASK_NOTIFICATION_TOPIC'],
            Message=message,
            Subject='Task Reminder'
        )

    return {
        'statusCode': 200,
        'body': 'Reminders sent successfully.'
    }