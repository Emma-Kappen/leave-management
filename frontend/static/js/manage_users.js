document.addEventListener('DOMContentLoaded', () => {
    const userListTableBody = document.querySelector('.user-list-table tbody');
    const noUsersMessage = document.querySelector('.no-users-message');

    // Function to fetch all user accounts from the backend
    async function fetchAllUsers() {
        try {
            const response = await fetch('/admin/users'); // Updated endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching user accounts:', error);
            userListTableBody.innerHTML = `<tr><td colspan="6" class="error-message">Failed to load user accounts. Please try again later.</td></tr>`;
            return [];
        }
    }

    // Function to display user accounts in the table
    function displayUsers(users) {
        if (users && users.length > 0) {
            noUsersMessage.style.display = 'none';
            userListTableBody.innerHTML = users.map(user => `
                <tr>
                    <td>${user.user_id}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>${user.role}</td>
                    <td>${user.department || '-'}</td>
                    <td class="action-buttons">
                        <a href="/templates/admin/edit_user.html?id=${user.user_id}" class="action-button">Edit</a>
                        <button class="action-button delete-button" data-user-id="${user.user_id}">Delete</button>
                    </td>
                </tr>
            `).join('');

            // Add event listeners to the delete buttons
            addDeleteEventListeners();

        } else {
            userListTableBody.innerHTML = '';
            noUsersMessage.style.display = 'block';
        }
    }

    // Function to handle delete user action
    function addDeleteEventListeners() {
        const deleteButtons = document.querySelectorAll('.delete-button');
        deleteButtons.forEach(button => {
            button.addEventListener('click', async (event) => {
                const userId = event.target.dataset.userId;
                if (confirm(`Are you sure you want to delete user with ID: ${userId}?`)) {
                    await deleteUser(userId);
                }
            });
        });
    }

    // Function to send the delete user request to the backend
    async function deleteUser(userId) {
        try {
            const response = await fetch(`/admin/users/${userId}`, { // Updated endpoint
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // After successful deletion, refresh the user list
            fetchAllUsers().then(displayUsers);
        } catch (error) {
            console.error(`Error deleting user with ID ${userId}:`, error);
            alert(`Failed to delete user. Please try again.`);
        }
    }

    // Fetch and display user accounts when the page loads
    fetchAllUsers().then(displayUsers);
});