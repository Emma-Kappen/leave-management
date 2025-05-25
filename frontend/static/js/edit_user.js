document.addEventListener('DOMContentLoaded', () => {
    const editUserForm = document.getElementById('edit-user-form');
    const userIdInput = document.getElementById('user_id');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const roleSelect = document.getElementById('role');
    const departmentInput = document.getElementById('department');

    // Function to get user ID from URL parameters
    function getUserIdFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }

    // Function to fetch user data for editing
    async function fetchUserData(userId) {
        try {
            const response = await fetch(`/admin/users/${userId}`); // Updated endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const userData = await response.json();
            return userData;
        } catch (error) {
            console.error('Error fetching user data:', error);
            alert('Failed to load user data for editing.');
            window.location.href = '/templates/admin/manage_users.html'; // Redirect back
            return null;
        }
    }

    // Populate the form with user data
    async function populateForm() {
        const userId = getUserIdFromUrl();
        if (userId) {
            const userData = await fetchUserData(userId);
            if (userData) {
                userIdInput.value = userData.user_id;
                nameInput.value = userData.name;
                emailInput.value = userData.email;
                roleSelect.value = userData.role;
                departmentInput.value = userData.department || '';
            }
        } else {
            alert('Invalid user ID.');
            window.location.href = '/templates/admin/manage_users.html'; // Redirect back
        }
    }

    // Event listener for form submission (saving changes)
    editUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(editUserForm);
        const userData = Object.fromEntries(formData.entries());
        const userId = getUserIdFromUrl();

        if (userId) {
            try {
                const response = await fetch(`/admin/users/${userId}`, {
                    method: 'PUT', // Updated method
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData),
                });

                if (response.ok) {
                    alert('User details updated successfully!');
                    window.location.href = '/templates/admin/manage_users.html'; // Redirect back
                } else {
                    const errorData = await response.json();
                    alert(`Failed to update user: ${errorData.error || 'An error occurred.'}`);
                }
            } catch (error) {
                console.error('Error updating user:', error);
                alert('Failed to update user. Please try again.');
            }
        } else {
            alert('Invalid user ID for update.');
        }
    });

    populateForm();
});