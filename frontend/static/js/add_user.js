document.addEventListener('DOMContentLoaded', () => {
    const addUserForm = document.getElementById('add-user-form');

    addUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(addUserForm);
        const userData = Object.fromEntries(formData.entries());

        try {
            // Update the endpoint to match your Flask backend route
            let endpoint = '/admin/students';
            if (userData.role === 'faculty') {
                endpoint = '/admin/faculty';
            }
            const response = await fetch(endpoint, {
                method: 'POST',
                body: JSON.stringify(userData),
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                alert('User added successfully!');
                window.location.href = '/templates/admin/manage_users.html'; // Redirect back to manage users page
            } else {
                const errorData = await response.json();
                alert(`Failed to add user: ${errorData.message || 'An error occurred.'}`);
            }
        } catch (error) {
            console.error('Error adding user:', error);
            alert('Failed to add user. Please try again.');
        }
    });

    // Pre-fill form data for demonstration (remove this in production)
    const userData = {
        role: 'student', // or 'faculty'
        usn: 'S12345', // For students
        id: 'FAC001', // For faculty
        name: 'John Doe',
        email: 'john.doe@example.com',
        password: 'securepassword',
        dept_id: 1, // For students
        designation: 'Professor', // For faculty
        supervisor_id: 'FAC002' // For faculty
    };

    // Fill the form with userData
    Object.keys(userData).forEach(key => {
        const field = addUserForm.querySelector(`[name="${key}"]`);
        if (field) {
            field.value = userData[key];
        }
    });
});