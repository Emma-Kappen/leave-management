document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logout-button');
    const userRoleElement = document.getElementById('user-role');
    const navBar = document.getElementById('nav-bar'); // Add this element in your layout.html
    const loginForm = document.getElementById('login-form');

    // Utility function for API calls with global error handling
    async function apiFetch(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error during API call to ${url}:`, error);
            alert(`An error occurred: ${error.message}`);
            throw error; // Re-throw the error for specific handling if needed
        }
    }

    // Function to handle logout
    async function logout() {
        try {
            await apiFetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            alert('Logged out successfully!');
            window.location.href = '/templates/login/index.html'; // Redirect to login page
        } catch (error) {
            console.error('Error during logout:', error);
        }
    }

    // Function to fetch the current user's role and update navigation
    async function fetchUserRoleAndUpdateNav() {
        try {
            const data = await apiFetch('/auth/user-role');
            if (userRoleElement) {
                userRoleElement.textContent = `Role: ${data.role}`;
            }

            // Update navigation based on role
            if (navBar) {
                if (data.role === 'Student') {
                    navBar.innerHTML = `
                        <a href="/templates/student/dashboard.html">Dashboard</a>
                        <a href="/templates/student/apply_leave.html">Apply Leave</a>
                        <a href="/templates/student/leave_status.html">Leave Status</a>
                    `;
                } else if (data.role === 'Faculty') {
                    navBar.innerHTML = `
                        <a href="/templates/faculty/faculty_dashboard.html">Dashboard</a>
                        <a href="/templates/faculty/leave_requests.html">Leave Requests</a>
                        <a href="/templates/faculty/leave_history.html">Leave History</a>
                    `;
                } else if (data.role === 'Admin') {
                    navBar.innerHTML = `
                        <a href="/templates/admin/admin_dashboard.html">Dashboard</a>
                        <a href="/templates/admin/manage_users.html">Manage Users</a>
                        <a href="/templates/admin/all_leaves.html">All Leaves</a>
                    `;
                }
            }
        } catch (error) {
            console.error('Error fetching user role:', error);
        }
    }

    // Attach logout functionality to the logout button
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // Fetch and display the user's role and update navigation
    fetchUserRoleAndUpdateNav();

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const userData = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });

                if (response.ok) {
                    const result = await response.json();
                    alert(result.message);
                    if (result.role === 'Student') {
                        window.location.href = '/templates/student/dashboard.html';
                    } else if (result.role === 'Faculty') {
                        window.location.href = '/templates/faculty/faculty_dashboard.html';
                    } else if (result.role === 'Admin') {
                        window.location.href = '/templates/admin/admin_dashboard.html';
                    }
                } else {
                    const errorData = await response.json();
                    alert(`Login failed: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});