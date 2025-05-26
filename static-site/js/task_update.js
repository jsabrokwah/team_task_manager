document.addEventListener('DOMContentLoaded', function() {
    // Check if user is authenticated
    if (!localStorage.getItem('access_token')) {
        window.location.href = 'index.html';
        return;
    }
    
    const taskSelect = document.getElementById('task-select');
    const taskUpdateForm = document.getElementById('task-update-form');
    
    // Load user's tasks
    function loadUserTasks() {
        fetch(`${config.apiBaseUrl}/tasks/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch tasks');
            return response.json();
        })
        .then(tasks => {
            taskSelect.innerHTML = '<option value="">Select a task</option>';
            
            if (tasks && tasks.length > 0) {
                tasks.forEach(task => {
                    const option = document.createElement('option');
                    option.value = task.task_id;
                    option.textContent = `${task.title} (Current: ${task.status})`;
                    taskSelect.appendChild(option);
                });
            } else {
                const option = document.createElement('option');
                option.disabled = true;
                option.textContent = 'No tasks available';
                taskSelect.appendChild(option);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to load tasks', 'error');
        });
    }
    
    // Handle form submission
    taskUpdateForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const taskId = taskSelect.value;
        const newStatus = document.getElementById('status').value;
        
        if (!taskId || !newStatus) {
            showAlert('Please select a task and status', 'error');
            return;
        }
        
        fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ status: newStatus })
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to update task');
            return response.json();
        })
        .then(() => {
            showAlert('Task updated successfully', 'success');
            taskUpdateForm.reset();
            loadUserTasks(); // Reload tasks with updated status
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to update task', 'error');
        });
    });
    
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
    
    // Initialize the page
    loadUserTasks();
});