// filepath: /home/jsabrokwah/Desktop/GTP_DevOps/task_management_system/static-site/js/tasks.js

const apiBaseUrl = 'https://your-api-url.com'; // Replace with your actual API URL

// Function to create a new task
async function createTask(taskData) {
    try {
        const response = await fetch(`${apiBaseUrl}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });
        if (!response.ok) {
            throw new Error('Failed to create task');
        }
        const task = await response.json();
        return task;
    } catch (error) {
        console.error(error);
    }
}

// Function to update an existing task
async function updateTask(taskId, updates) {
    try {
        const response = await fetch(`${apiBaseUrl}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updates),
        });
        if (!response.ok) {
            throw new Error('Failed to update task');
        }
        const updatedTask = await response.json();
        return updatedTask;
    } catch (error) {
        console.error(error);
    }
}

// Function to delete a task
async function deleteTask(taskId) {
    try {
        const response = await fetch(`${apiBaseUrl}/tasks/${taskId}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete task');
        }
        return true;
    } catch (error) {
        console.error(error);
    }
}

// Function to fetch all tasks
async function fetchAllTasks() {
    try {
        const response = await fetch(`${apiBaseUrl}/tasks`);
        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }
        const tasks = await response.json();
        return tasks;
    } catch (error) {
        console.error(error);
    }
}

// Function to fetch tasks assigned to a specific user
async function fetchUserTasks(userId) {
    try {
        const response = await fetch(`${apiBaseUrl}/tasks/me`, {
            headers: {
                'User-ID': userId, // Assuming you send user ID in headers
            },
        });
        if (!response.ok) {
            throw new Error('Failed to fetch user tasks');
        }
        const tasks = await response.json();
        return tasks;
    } catch (error) {
        console.error(error);
    }
}