from datetime import datetime, timezone
import boto3
import uuid
import os
import logging
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger(__name__)

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
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            
            # Generate user_id if not provided
            if 'user_id' not in user_data:
                user_data['user_id'] = User.generate_user_id()
                
            # Set default role if not provided
            if 'role' not in user_data:
                user_data['role'] = 'member'
                
            item = {
                'user_id': user_data['user_id'],
                'role': user_data['role'],
                'name': user_data['name'],
                'email': user_data['email'],
                'hashed_password': user_data['hashed_password'],
                'refresh_token': user_data.get('refresh_token'),
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            
            table.put_item(Item=item)
            return True
        except ClientError as e:
            logger.error(f"Error creating user: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating user: {e}")
            return False

    @staticmethod
    def get_user(user_id):
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            response = table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Error getting user: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user: {e}")
            return None

    @staticmethod
    def get_all_users():
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            response = table.scan()
            items = response.get('Items', [])
            
            # Handle pagination for large result sets
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                items.extend(response.get('Items', []))
                
            return items
        except ClientError as e:
            logger.error(f"Error getting all users: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting all users: {e}")
            return []

    @staticmethod
    def get_user_by_email(email):
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            response = table.scan(
                FilterExpression="email = :email",
                ExpressionAttributeValues={":email": email}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            logger.error(f"Error getting user by email: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user by email: {e}")
            return None

    @staticmethod
    def get_user_by_role(role):
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            response = table.scan(
                FilterExpression="role = :role",
                ExpressionAttributeValues={":role": role}
            )
            items = response.get('Items', [])
            return items
        except ClientError as e:
            logger.error(f"Error getting user by role: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error getting user by role: {e}")
            return []
        
    @staticmethod
    def update_user(user_id, update_data):
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)

            # Check if user exists
            user = User.get_user(user_id)
            if not user:
                return False

            update_expression = "SET "
            expression_attribute_values = {}

            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value

            # Add updated_at field
            update_expression += "updated_at = :updated_at"
            expression_attribute_values[":updated_at"] = datetime.now(timezone.utc).isoformat()

            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
            return True
        except ClientError as e:
            logger.error(f"Error updating user: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error updating user: {e}")
            return False

    @staticmethod
    def delete_user(user_id):
        dynamodb = boto3.resource('dynamodb')
        try:
            users_table_name = os.environ.get('USERS_TABLE', 'Users')
            table = dynamodb.Table(users_table_name)
            
            # Check if user exists
            user = User.get_user(user_id)
            if not user:
                return False
                
            table.delete_item(Key={'user_id': user_id})
            return True
        except ClientError as e:
            logger.error(f"Error deleting user: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting user: {e}")
            return False
    
    @staticmethod
    def generate_user_id():
        return f"user_{uuid.uuid4().hex}"
        
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'role': self.role,
            'name': self.name,
            'email': self.email,
            # Don't include hashed_password for security
            'refresh_token': self.refresh_token
        }