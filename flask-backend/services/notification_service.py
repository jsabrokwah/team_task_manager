class NotificationService:
    def __init__(self, sns_client):
        self.sns_client = sns_client

    def send_task_assignment_notification(self, user_email, task_title):
        subject = "New Task Assigned"
        message = f"You have been assigned a new task: {task_title}."
        self.send_notification(user_email, subject, message)

    def send_reminder_notification(self, user_email, task_title, due_date):
        subject = "Task Reminder"
        message = f"Reminder: The task '{task_title}' is due on {due_date}."
        self.send_notification(user_email, subject, message)

    def send_notification(self, user_email, subject, message):
        response = self.sns_client.publish(
            TopicArn='arn:aws:sns:your-region:your-account-id:TaskNotifications',
            Message=message,
            Subject=subject,
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': user_email
                }
            }
        )
        return response
    
    