async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            alert('Logged out successfully!');
            window.location.href = '/frontend/templates/login/student_login.html'; // Redirect to login page
        } else {
            alert('Failed to log out. Please try again.');
        }
    } catch (error) {
        console.error('Error during logout:', error);
        alert('An error occurred while logging out.');
    }
}

// Call the logout function when the logout button is clicked
document.getElementById('logout-button').addEventListener('click', logout);

// You would add other JavaScript functionality for the student dashboard here,
// such as fetching and updating data dynamically.

async function fetchDashboardData() {
    try {
        const response = await fetch('/student/leave-status'); // Example endpoint
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Dashboard Data:', data);
        // Add logic to display data in the dashboard
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
    }
}

// Fetch dashboard data when the page loads
document.addEventListener('DOMContentLoaded', fetchDashboardData);