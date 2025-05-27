# Task Management System.

## Problem Definition:
Design and implement a Task Management System for a field team using AWS serverless services. The system should allow an admin to create and assign tasks to team members. Team members log in to view and update their assigned tasks, while the admin oversees all tasks, team assignments, and deadlines. The system must handle task notifications, status updates, and deadline tracking efficiently, ensuring a seamless workflow.

## Phase 1: Planning & Design

**Tasks:**

* Gather detailed requirements and user stories for admin vs. member roles.
* Define DynamoDB table schemas (e.g., **Users**, **Tasks**, with primary keys and GSI for querying by user or status).
* Design API contract (REST endpoints for login, CRUD tasks, status updates). ([AWS Documentation][1])
* Sketch notification flows (task‐assigned, reminders, overdue alerts).
* Define auth model (JWT issuance in Flask backed by DynamoDB “Users” table).
* Create high-level Terraform/SAM template outline for all resources.

**Deliverables:**

* Requirements doc & data-model ERD.
* OpenAPI/Swagger spec.
* Initial SAM template skeleton.

---

## Phase 2: Infrastructure Setup

**Tasks:**

1. **Version Control:** Create CodeCommit repo and push SAM project scaffold. ([AWS Documentation][2])
2. **SAM local:** Install SAM CLI and verify `sam local start-api` and `sam local start-lambda`. ([AWS Documentation][3], [AWS Documentation][4])
3. **DynamoDB:** Define `Users` & `Tasks` tables in SAM template. ([AWS Documentation][5])
4. **S3 Static Hosting:** Configure an S3 bucket for website hosting (HTML/JS/CSS). ([AWS Documentation][6])
5. **API Gateway & Lambda:**

   * Define HTTP API in SAM.
   * Attach to Flask Lambda functions. ([AWS Documentation][7])
6. **SNS & EventBridge:**

   * Create SNS topics for notifications. ([AWS Documentation][8])
   * Define EventBridge rules for scheduled reminders. ([AWS Documentation][9])

**Deliverables:**

* SAM template deployed to dev environment.
* All resources provisioned (via `sam deploy --guided`).

---

## Phase 3: Backend Development

**Tasks:**

* **Flask App:**

  * Implement authentication endpoints (`/user/create`, `/user/update/{user_id}`, `/user/delete/{user_id}`, `/user/all`, ` /user/{user_id}`, `/login`, `/refresh`, `/logout`,`/signup` ) issuing JWTs and storing refresh tokens in DynamoDB.
  * CRUD endpoints for Tasks: create, assign, list by user/admin, update status.
* **Integrations:**

  * DynamoDB access via AWS SDK for Python (boto3).
  * SNS publish on task creation and status change.
  * EventBridge scheduler Lambda for deadline reminders.
* **Unit Tests:** Use pytest and `sam local invoke` to validate. ([AWS Documentation][10])

**Deliverables:**

* Flask app code in SAM structure.
* Unit test coverage report.

---

## Phase 4: Frontend Development

**Tasks:**

* **Design:**

  * Create wireframes for the following pages:
    * **Login Page:** A simple form for user authentication.
    * **Admin Dashboard:** Displays task statistics, user management, and task creation forms.
    * **Member Dashboard:** Displays assigned tasks and allows updates.
    * **Task List View:** A table or card-based layout for viewing tasks.
    * **Task Update Form:** A form to update task details (e.g., status, description).
  
* **Development:**

  * Build static HTML/CSS/JS pages:
    * **Login Page:** Includes fields for email and password, with client-side validation.
    * **Admin Dashboard:** Includes task creation and user management sections.
    * **Member Dashboard:** Displays assigned tasks with options to update status.
    * **Task List View:** Fetches and displays tasks using API calls.
    * **Task Update Form:** Allows users to update task details.
  * Implement responsive design for mobile and desktop views.
  * Use JavaScript to make client-side API calls to the backend endpoints with JWT authentication headers.

* **Hosting:**

  * Host the static site files on an S3 bucket configured for public read access.
  * Use SAM to automate deployment and invalidate CloudFront cache (if applicable).

* **Testing:**

  * Test the frontend with mock API responses to ensure proper integration.
  * Validate JWT authentication flows and error handling.

**Deliverables:**

* Wireframes for all pages.
* Static site files in a dedicated CodeCommit branch.
* Fully functional site deployed to S3 with correct bucket policy for public read.
* Documentation for frontend setup and API integration.

---

## Additional Notes:

* The frontend will use modern JavaScript (ES6+), html, and css files. Do not use any frontend framework
* The design will prioritize simplicity and usability, ensuring that both admins and team members can easily navigate the system.


## Phase 5: Integration & Testing

**Tasks:**

* **End-to-end tests:** Using Postman/Newman or Cypress against local SAM endpoints.
* **Staging deploy:** Deploy SAM to a staging AWS account.
* **Load testing:** Simple scripts to simulate multiple users.
* **Security review:** Validate JWT flows, CORS policies, bucket permissions.

**Deliverables:**

* Test reports and bug backlog.
* Hardened SAM templates with best-practice IAM roles.

---

## Phase 6: CI/CD Pipeline

**Tasks:**

1. **CodePipeline:**

   * **Source Stage:** CodeCommit trigger on push. ([AWS Documentation][11])
   * **Build Stage:** CodeBuild project executing `sam build` and running tests. ([Amazon Web Services, Inc.][12])
   * **Deploy Stage:** `sam deploy` via CloudFormation actions.
2. **Artifact Store:** S3 bucket for build artifacts.
3. **Notifications:** Use EventBridge or CodePipeline notifications when pipeline fails/succeeds.
4. **Manual approvals** (optional) before prod deploy.

**Deliverables:**

* Fully automated pipeline in AWS console.
* Branch-based workflows (e.g., `dev` → staging, `main` → prod).

---

## Phase 7: Monitoring, Alerts & Maintenance

**Tasks:**

* **CloudWatch Logs & Metrics:**

  * Enable Lambda logging and API Gateway metrics. ([AWS Documentation][13])
* **Alarms:**

  * Create CloudWatch alarms for function errors or throttling (SNS to notify admin).
* **Documentation:**

  * Update README, API docs, and runbooks.
* **Iterate:**

  * Plan sprints for feature enhancements and refactoring.

**Deliverables:**

* Operational runbook.
* Dashboard for key metrics.

---
