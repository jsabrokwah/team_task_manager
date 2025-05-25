from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

class User:
    def __init__(self, user_id, role, name, email, hashed_password, refresh_token=None):
        self.user_id = user_id
        self.role = role
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.refresh_token = refresh_token

    @staticmethod
    def create_user(user_data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        user_id = user_data['user_id']
        
        try:
            table.put_item(Item={
                'user_id': user_id,
                'role': user_data['role'],
                'name': user_data['name'],
                'email': user_data['email'],
                'hashed_password': user_data['hashed_password'],
                'refresh_token': user_data.get('refresh_token')
            })
            return True
        except ClientError as e:
            print(f"Error creating user: {e.response['Error']['Message']}")
            return False

    @staticmethod
    def get_user(user_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        
        try:
            response = table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting user: {e.response['Error']['Message']}")
            return None

    @staticmethod
    def get_all_users():
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        
        try:
            response = table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting all users: {e.response['Error']['Message']}")
            return []

    @staticmethod
    def get_user_by_email(email):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        
        try:
            response = table.scan(
                FilterExpression="email = :email",
                ExpressionAttributeValues={":email": email}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            print(f"Error getting user by email: {e.response['Error']['Message']}")
            return None

    @staticmethod
    def update_user(user_id, update_data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')

        update_expression = "SET "
        expression_attribute_values = {}

        for key, value in update_data.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value

        # Add updated_at field
        update_expression += "updated_at = :updated_at"
        expression_attribute_values[":updated_at"] = datetime.now(timezone.utc).isoformat()

        try:
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return True
        except ClientError as e:
            print(f"Error updating user: {e.response['Error']['Message']}")
            return False

    @staticmethod
    def delete_user(user_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        
        try:
            table.delete_item(Key={'user_id': user_id})
            return True
        except ClientError as e:
            print(f"Error deleting user: {e.response['Error']['Message']}")
            return False
    
    
    @staticmethod
    def generate_user_id():
        return 'user_'+str(datetime.now(datetime.timezone.utc).timestamp()).replace('.', '')+str(int(datetime.now(datetime.timezone.utc).microsecond))
    