class Task:
    def __init__(self, task_id, assigned_to, title, description, status, due_date, created_at=None, updated_at=None):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.created_at = created_at if created_at else self.get_current_timestamp()
        self.updated_at = updated_at if updated_at else self.get_current_timestamp()

    @staticmethod
    def get_current_timestamp():
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'assigned_to': self.assigned_to,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data['task_id'],
            assigned_to=data['assigned_to'],
            title=data['title'],
            description=data['description'],
            status=data['status'],
            due_date=data['due_date'],
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )