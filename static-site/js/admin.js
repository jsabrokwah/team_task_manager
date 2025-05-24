// This script handles user management and task display in the admin panel
document.addEventListener('DOMContentLoaded', function() {
    const createUserForm = document.getElementById('createUserForm');
    const updateUserForm = document.getElementById('updateUserForm');
    const deleteUserForm = document.getElementById('deleteUserForm');
    const taskList = document.getElementById('taskList');

    // Create User
    if (createUserForm) {
        createUserForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(createUserForm);
            const userData = Object.fromEntries(formData.entries());

            fetch('/user/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                createUserForm.reset();
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Update User
    if (updateUserForm) {
        updateUserForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const userId = updateUserForm.querySelector('input[name="user_id"]').value;
            const formData = new FormData(updateUserForm);
            const userData = Object.fromEntries(formData.entries());

            fetch(`/user/update/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                updateUserForm.reset();
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Delete User
    if (deleteUserForm) {
        deleteUserForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const userId = deleteUserForm.querySelector('input[name="user_id"]').value;

            fetch(`/user/delete/${userId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                deleteUserForm.reset();
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Fetch and display tasks
    function fetchTasks() {
        fetch('/tasks')
            .then(response => response.json())
            .then(tasks => {
                taskList.innerHTML = '';
                tasks.forEach(task => {
                    const li = document.createElement('li');
                    li.textContent = `${task.title} - Assigned to: ${task.assigned_to}`;
                    taskList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching tasks:', error));
    }

    fetchTasks();
});