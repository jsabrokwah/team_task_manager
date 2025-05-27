# Testing the Task Management System Locally

This guide explains how to set up and test the Task Management System on your local machine.

## Prerequisites

1. Python 3.12
2. Node.js (optional, for running a local web server)
3. AWS CLI installed
4. DynamoDB Local

## Setting Up DynamoDB Local

1. Download DynamoDB Local from the [AWS Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
2. Extract the downloaded archive to a directory of your choice
3. Start DynamoDB Local:
   ```
   java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
   ```

## Setting Up the Backend

1. Run the local setup script:
   ```
   chmod +x local_setup.sh
   ./local_setup.sh
   ```

2. Activate the virtual environment:
   ```
   cd flask-backend
   source venv/bin/activate
   ```

3. Run the Flask application:
   ```
   python local_app.py
   ```
   The API will be available at http://127.0.0.1:5000/

## Setting Up the Frontend

1. Update the frontend configuration to use the local API:
   - Open `static-site/index.html` in a text editor
   - Change the script import from `config.js` to `local_config.js`:
     ```html
     <script src="js/local_config.js"></script>
     ```

2. Serve the static site using a local web server:
   
   Using Python:
   ```
   cd static-site
   python -m http.server 8080
   ```
   
   Using Node.js (if you have it installed):
   ```
   cd static-site
   npx http-server -p 8080
   ```

   Then open http://localhost:8080 in your browser.

## Creating Initial Data

1. Create an admin user:
   ```
   curl -X POST http://127.0.0.1:5000/user/create \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123", "email": "admin@example.com", "role": "admin"}'
   ```

2. Login to get an access token:
   ```
   curl -X POST http://127.0.0.1:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
   ```

3. Create a task (replace `YOUR_ACCESS_TOKEN` with the token from the login response):
   ```
   curl -X POST http://127.0.0.1:5000/tasks \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{"title": "Test Task", "description": "This is a test task", "status": "pending", "due_date": "2023-12-31"}'
   ```

## Testing

Run the tests using pytest:
```
cd flask-backend
pytest
```

## Troubleshooting

1. **DynamoDB Connection Issues**:
   - Make sure DynamoDB Local is running
   - Check that the endpoint URL is correctly set to `http://localhost:8000`

2. **CORS Issues**:
   - If you encounter CORS errors, make sure the Flask CORS configuration is properly set up
   - Try using a browser extension to disable CORS for testing

3. **JWT Token Issues**:
   - Check that the JWT secret key is properly set in the `.env` file
   - Ensure token expiration times are reasonable for development