document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch(`${config.apiBaseUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            window.location.href = 'member_dashboard.html';
        })
        .catch(error => {
            loginMessage.textContent = error.message;
            loginMessage.style.color = 'red';
        });
    });

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            const token = localStorage.getItem('access_token');
            
            fetch(`${config.apiBaseUrl}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = 'index.html';
            })
            .catch(() => {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = 'index.html';
            });
        });
    }
});