from datetime import datetime

class TaskService:
    def __init__(self, dynamodb_resource):
        self.dynamodb = dynamodb_resource
        self.tasks_table = self.dynamodb.Table('Tasks')

    def create_task(self, task_data):
        task_id = task_data.get('task_id')
        assigned_to = task_data.get('assigned_to')
        title = task_data.get('title')
        description = task_data.get('description')
        status = task_data.get('status')
        due_date = task_data.get('due_date')

        item = {
            'task_id': task_id,
            'assigned_to': assigned_to,
            'title': title,
            'description': description,
            'status': status,
            'due_date': due_date,
            'created_at': datetime.now(datetime.timezone.utc).isoformat(),
            'updated_at': datetime.now(datetime.timezone.utc).isoformat()
        }

        self.tasks_table.put_item(Item=item)
        return item

    def get_task(self, task_id):
        response = self.tasks_table.get_item(Key={'task_id': task_id})
        return response.get('Item')

    def update_task(self, task_id, updates):
        update_expression = "SET "
        expression_attribute_values = {}
        
        for key, value in updates.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(", ")
        update_expression += ", updated_at = :updated_at"
        expression_attribute_values[":updated_at"] = datetime.now(datetime.timezone.utc).isoformat()

        self.tasks_table.update_item(
            Key={'task_id': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    def delete_task(self, task_id):
        self.tasks_table.delete_item(Key={'task_id': task_id})

    def list_tasks(self, assigned_to=None, status=None):
        filter_expression = []
        expression_attribute_values = {}

        if assigned_to:
            filter_expression.append("assigned_to = :assigned_to")
            expression_attribute_values[":assigned_to"] = assigned_to

        if status:
            filter_expression.append("status = :status")
            expression_attribute_values[":status"] = status


        try:
            scan_kwargs = {}
            if filter_expression:
                scan_kwargs['FilterExpression'] = " AND ".join(filter_expression)
                scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values

            response = self.tasks_table.scan(**scan_kwargs)
            return response.get('Items', [])
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")
            return []
    