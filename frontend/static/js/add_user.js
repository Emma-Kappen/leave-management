// Add User JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-user-form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            role: document.getElementById('role').value,
            department: document.getElementById('department').value
        };
        
        fetch('/admin/add-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add user');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.href = '/admin/manage-users';
        })
        .catch(error => {
            console.error('Error adding user:', error);
            alert('Failed to add user. Please try again.');
        });
    });
});