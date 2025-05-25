// Edit User JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('edit-user-form');
    const userId = document.getElementById('user_id').value;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            role: document.getElementById('role').value,
            department: document.getElementById('department').value
        };
        
        fetch(`/admin/edit-user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update user');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.href = '/admin/manage-users';
        })
        .catch(error => {
            console.error('Error updating user:', error);
            alert('Failed to update user. Please try again.');
        });
    });
});