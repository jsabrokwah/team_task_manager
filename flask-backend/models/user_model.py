from datetime import datetime
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
    def update_user(user_id, update_data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Users')
        
        update_expression = "SET "
        expression_attribute_values = {}
        
        for key, value in update_data.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(", ")
        
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