// Utility functions for API calls and UI interactions

function apiCall(endpoint, method, data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    return fetch(`${config.apiBaseUrl}${endpoint}`, options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('API call error:', error);
            throw error;
        });
}

function showAlert(message, type = 'info') {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
    document.body.appendChild(alertBox);
    
    setTimeout(() => {
        alertBox.remove();
    }, 3000);
}

function getUserIdFromToken() {
    const token = localStorage.getItem('access_token');
    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.sub || payload.user_id;
    } catch (error) {
        console.error('Error parsing token:', error);
        return null;
    }
}