document.addEventListener('DOMContentLoaded', function() {
    const taskTableBody = document.querySelector('#task-table tbody');
    
    // Check if user is authenticated
    if (!localStorage.getItem('access_token')) {
        window.location.href = 'index.html';
        return;
    }

    // Fetch and display tasks assigned to the user
    function loadUserTasks() {
        fetch(`${config.apiBaseUrl}/tasks/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch tasks');
            }
            return response.json();
        })
        .then(tasks => {
            taskTableBody.innerHTML = '';
            
            if (tasks && tasks.length > 0) {
                tasks.forEach(task => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${task.title}</td>
                        <td>${task.description}</td>
                        <td>${task.status}</td>
                        <td>${task.due_date}</td>
                        <td>
                            <button class="update-task" data-task-id="${task.task_id}">Update Status</button>
                        </td>
                    `;
                    taskTableBody.appendChild(row);
                });
                
                // Add event listeners to update buttons
                document.querySelectorAll('.update-task').forEach(button => {
                    button.addEventListener('click', function() {
                        const taskId = this.getAttribute('data-task-id');
                        const newStatus = prompt('Enter new status (e.g., In Progress, Completed):');
                        if (newStatus) {
                            updateTaskStatus(taskId, newStatus);
                        }
                    });
                });
            } else {
                taskTableBody.innerHTML = '<tr><td colspan="5">No tasks assigned to you.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to load tasks', 'error');
        });
    }

    // Update task status
    function updateTaskStatus(taskId, newStatus) {
        fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ status: newStatus })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update task');
            }
            return response.json();
        })
        .then(() => {
            showAlert('Task updated successfully', 'success');
            loadUserTasks(); // Reload tasks
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to update task', 'error');
        });
    }

    // Initialize page
    loadUserTasks();
    
    // Add logout functionality
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            fetch(`${config.apiBaseUrl}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            })
            .finally(() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = 'index.html';
            });
        });
    }
});