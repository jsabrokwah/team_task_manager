
document.addEventListener('DOMContentLoaded', function() {
    const userTasksContainer = document.getElementById('user-tasks');
    const updateTaskButtons = document.querySelectorAll('.update-task');

    // Fetch and display tasks assigned to the user
    function fetchUserTasks() {
        fetch('/api/tasks/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                data.forEach(task => {
                    const taskElement = document.createElement('div');
                    taskElement.classList.add('task');
                    taskElement.innerHTML = `
                        <h3>${task.title}</h3>
                        <p>${task.description}</p>
                        <p>Status: <span class="task-status">${task.status}</span></p>
                        <p>Due Date: ${task.due_date}</p>
                        <button class="update-task" data-task-id="${task.task_id}">Update Status</button>
                    `;
                    userTasksContainer.appendChild(taskElement);
                });
            } else {
                userTasksContainer.innerHTML = '<p>No tasks assigned.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            userTasksContainer.innerHTML = '<p>Error loading tasks.</p>';
        });
    }

    // Update task status
    function updateTaskStatus(taskId, newStatus) {
        fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ status: newStatus })
        })
        .then(response => {
            if (response.ok) {
                alert('Task status updated successfully.');
                location.reload(); // Reload to fetch updated tasks
            } else {
                alert('Failed to update task status.');
            }
        })
        .catch(error => {
            console.error('Error updating task:', error);
        });
    }

    // Event listener for update buttons
    updateTaskButtons.forEach(button => {
        button.addEventListener('click', function() {
            const taskId = this.getAttribute('data-task-id');
            const newStatus = prompt('Enter new status (e.g., In Progress, Completed):');
            if (newStatus) {
                updateTaskStatus(taskId, newStatus);
            }
        });
    });

    // Initial fetch of user tasks
    fetchUserTasks();
});