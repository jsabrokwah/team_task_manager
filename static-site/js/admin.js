document.addEventListener('DOMContentLoaded', function() {
    // Check if user is authenticated
    if (!localStorage.getItem('access_token')) {
        window.location.href = 'index.html';
        return;
    }
    
    const taskTableBody = document.querySelector('#admin-task-table tbody');
    const userTableBody = document.querySelector('#admin-user-table tbody');
    const userSelect = document.getElementById('assigned_to');
    const createTaskForm = document.getElementById('create-task-form');
    
    // Load all tasks
    function loadAllTasks() {
        fetch(`${config.apiBaseUrl}/tasks`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch tasks');
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
                        <td>${task.assigned_to || 'Unassigned'}</td>
                        <td>${task.due_date}</td>
                        <td>
                            <button class="edit-task" data-task-id="${task.task_id}">Edit</button>
                            <button class="delete-task" data-task-id="${task.task_id}">Delete</button>
                        </td>
                    `;
                    taskTableBody.appendChild(row);
                });
                
                // Add event listeners to buttons
                addTaskButtonListeners();
            } else {
                taskTableBody.innerHTML = '<tr><td colspan="6">No tasks available</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to load tasks', 'error');
        });
    }
    
    // Load all users
    function loadAllUsers() {
        fetch(`${config.apiBaseUrl}/user/all`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch users');
            return response.json();
        })
        .then(users => {
            userTableBody.innerHTML = '';
            userSelect.innerHTML = '<option value="">Select User</option>';
            
            if (users && users.length > 0) {
                users.forEach(user => {
                    // Add to user table
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.name || user.username}</td>
                        <td>${user.email}</td>
                        <td>${user.role || 'Member'}</td>
                        <td>
                            <button class="edit-user" data-user-id="${user.user_id}">Edit</button>
                            <button class="delete-user" data-user-id="${user.user_id}">Delete</button>
                        </td>
                    `;
                    userTableBody.appendChild(row);
                    
                    // Add to select dropdown
                    const option = document.createElement('option');
                    option.value = user.user_id;
                    option.textContent = user.name || user.email;
                    userSelect.appendChild(option);
                });
                
                // Add event listeners to buttons
                addUserButtonListeners();
            } else {
                userTableBody.innerHTML = '<tr><td colspan="4">No users available</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to load users', 'error');
        });
    }
    
    // Add event listeners to task buttons
    function addTaskButtonListeners() {
        // Edit task buttons
        document.querySelectorAll('.edit-task').forEach(button => {
            button.addEventListener('click', function() {
                const taskId = this.getAttribute('data-task-id');
                // Implement edit functionality
                alert('Edit task functionality to be implemented');
            });
        });
        
        // Delete task buttons
        document.querySelectorAll('.delete-task').forEach(button => {
            button.addEventListener('click', function() {
                const taskId = this.getAttribute('data-task-id');
                if (confirm('Are you sure you want to delete this task?')) {
                    fetch(`${config.apiBaseUrl}/tasks/${taskId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Failed to delete task');
                        return response.json();
                    })
                    .then(() => {
                        showAlert('Task deleted successfully', 'success');
                        loadAllTasks();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showAlert('Failed to delete task', 'error');
                    });
                }
            });
        });
    }
    
    // Add event listeners to user buttons
    function addUserButtonListeners() {
        // Edit user buttons
        document.querySelectorAll('.edit-user').forEach(button => {
            button.addEventListener('click', function() {
                const userId = this.getAttribute('data-user-id');
                // Implement edit functionality
                alert('Edit user functionality to be implemented');
            });
        });
        
        // Delete user buttons
        document.querySelectorAll('.delete-user').forEach(button => {
            button.addEventListener('click', function() {
                const userId = this.getAttribute('data-user-id');
                if (confirm('Are you sure you want to delete this user?')) {
                    fetch(`${config.apiBaseUrl}/user/delete/${userId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                        }
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Failed to delete user');
                        return response.json();
                    })
                    .then(() => {
                        showAlert('User deleted successfully', 'success');
                        loadAllUsers();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showAlert('Failed to delete user', 'error');
                    });
                }
            });
        });
    }
    
    // Handle task creation form submission
    if (createTaskForm) {
        createTaskForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const taskData = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                assigned_to: document.getElementById('assigned_to').value,
                due_date: document.getElementById('due_date').value,
                status: 'New'
            };
            
            fetch(`${config.apiBaseUrl}/tasks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(taskData)
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to create task');
                return response.json();
            })
            .then(() => {
                showAlert('Task created successfully', 'success');
                createTaskForm.reset();
                loadAllTasks();
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Failed to create task', 'error');
            });
        });
    }
    
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
    loadAllTasks();
    loadAllUsers();
});