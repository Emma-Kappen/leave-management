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
            window.location.href = '/templates/login/faculty_login.html'; // Redirect to login page
        } else {
            alert('Failed to log out. Please try again.');
        }
    } catch (error) {
        console.error('Error during logout:', error);
        alert('An error occurred while logging out.');
    }
}

// Fetch pending leave requests
async function fetchPendingLeaveRequests() {
    try {
        const response = await fetch('/faculty/leave-requests');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const leaveRequests = await response.json();
        console.log('Pending Leave Requests:', leaveRequests);
        // Add logic to display leave requests in the dashboard
    } catch (error) {
        console.error('Error fetching leave requests:', error);
    }
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchPendingLeaveRequests();
});