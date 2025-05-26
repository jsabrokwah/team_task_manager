// Task management functions

// Function to create a new task
async function createTask(taskData) {
    try {
        const response = await fetch(`${config.apiBaseUrl}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(taskData),
        });
        if (!response.ok) {
            throw new Error('Failed to create task');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// Function to update an existing task
async function updateTask(taskId, updates) {
    try {
        const response = await fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify(updates),
        });
        if (!response.ok) {
            throw new Error('Failed to update task');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// Function to delete a task
async function deleteTask(taskId) {
    try {
        const response = await fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to delete task');
        }
        return true;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// Function to fetch all tasks
async function fetchAllTasks() {
    try {
        const response = await fetch(`${config.apiBaseUrl}/tasks`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}

// Function to fetch tasks assigned to the current user
async function fetchUserTasks() {
    try {
        const response = await fetch(`${config.apiBaseUrl}/tasks/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        });
        if (!response.ok) {
            throw new Error('Failed to fetch user tasks');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}