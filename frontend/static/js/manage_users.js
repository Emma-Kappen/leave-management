// Manage Users JavaScript

// Load all users when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadUsers();
});

// Function to load all users
function loadUsers() {
    fetch('/admin/get-users', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to load users');
        }
        return response.json();
    })
    .then(users => {
        displayUsers(users);
    })
    .catch(error => {
        console.error('Error loading users:', error);
        document.querySelector('.no-users-message').style.display = 'block';
    });
}

// Function to display users in the table
function displayUsers(users) {
    const tableBody = document.querySelector('.user-list-table tbody');
    tableBody.innerHTML = '';
    
    if (users.length === 0) {
        document.querySelector('.no-users-message').style.display = 'block';
        return;
    }
    
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td>${user.department}</td>
            <td class="action-buttons">
                <a href="/admin/edit-user/${user.id}" class="action-button">Edit</a>
                <button onclick="deleteUser('${user.id}')" class="action-button">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Function to delete a user
function deleteUser(userId) {
    if (!confirm(`Are you sure you want to delete user ${userId}?`)) {
        return;
    }
    
    fetch(`/admin/delete-user/${userId}`, {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete user');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        loadUsers(); // Reload the user list
    })
    .catch(error => {
        console.error('Error deleting user:', error);
        alert('Failed to delete user. Please try again.');
    });
}