
# Task Management System - Requirements Document

## Overview

This system is designed to manage tasks for a field team using AWS serverless infrastructure. It includes two roles: Admin and Team Member. Admins manage all tasks and users. Team Members receive and update their task statuses.

---

## User Roles

### 1. Admin

- Create, read, update, delete (CRUD) tasks.
- Assign tasks to team members.
- View tasks by status, assignee, or due date.
- Receive notifications on overdue tasks or changes.
- Manage user accounts (Create, Update, Delete, List, Show).

### 2. Team Member

- Log in and authenticate.
- View tasks assigned to them.
- Update task statuses (e.g., In Progress, Completed).
- Receive reminders and alerts.

---

## Functional Requirements

### Authentication

- JWT-based login and token refresh.
- Role-based access control.
- Store hashed passwords and refresh tokens.

### Task Management

- CRUD operations for tasks.
- Assign and reassign tasks.
- Track task status and due dates.
- Automatic timestamping (created_at, updated_at).

### Notifications

- Task assignment triggers SNS notification.
- EventBridge triggers reminders before task deadlines.
- Notifications sent via email or SMS (configurable).

### Frontend

- HTML/CSS/JS-based static website.
- Login page and dashboards for both roles.
- Dynamic interaction via REST API using JWT.

---

## Non-Functional Requirements

- **Scalability:** Leverage AWS Lambda and API Gateway.
- **Availability:** Use DynamoDB with on-demand throughput.
- **Security:** JWT, hashed passwords, CORS, IAM roles.
- **Maintainability:** Use SAM templates and CodeCommit for version control.

---

## AWS Services

- **Lambda:** Business logic for API.
- **API Gateway:** Expose REST endpoints.
- **DynamoDB:** Store user and task data.
- **S3:** Host static frontend.
- **SNS:** Send notifications.
- **EventBridge:** Schedule reminders.
- **CloudWatch:** Logs and metrics.
- **CodePipeline:** CI/CD.

---

## DynamoDB Tables

### Users Table

- `user_id` (PK)
- `role`
- `name`
- `email`
- `hashed_password`
- `refresh_token`

### Tasks Table

- `task_id` (PK)
- `assigned_to` (FK - user_id)
- `title`
- `description`
- `status`
- `due_date`
- `created_at`
- `updated_at`

---

## API Endpoints

- `POST /user/create` (admin only)
- `PUT /user/update/{user_id}` (admin only)
- `DELETE /user/delete/{user_id}` (admin only)
- `GET /user/all` (admin only)
- `GET /user/{user_id}` (admin only)
- `POST /login`
- `POST /refresh`
- `POST /logout`
- `GET /tasks` (admin only)
- `GET /tasks/me` (member only)
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

---

## Notification Flows

- On task creation: Notify assigned user.
- 24 hours before due date: Send reminder.
- If overdue: Notify admin and assignee.

---


