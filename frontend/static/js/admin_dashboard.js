// Admin Dashboard JavaScript

// Logout function
function logout() {
    fetch('/auth/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = '/auth/admin-login';
    })
    .catch(error => {
        console.error('Logout failed:', error);
        window.location.href = '/auth/admin-login';
    });
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    fetch('/auth/check-auth', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            window.location.href = '/auth/admin-login';
            throw new Error('Not authenticated');
        }
        return response.json();
    })
    .then(data => {
        if (data.role !== 'admin') {
            window.location.href = data.redirect;
        }
    })
    .catch(error => {
        console.error('Authentication check failed:', error);
    });
});