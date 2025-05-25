// Student Dashboard JavaScript

// Check if user is authenticated
function checkAuth() {
    fetch('/auth/check-auth', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            // Redirect to login page if not authenticated
            window.location.href = '/auth/student-login';
            throw new Error('Not authenticated');
        }
        return response.json();
    })
    .then(data => {
        if (data.role !== 'student') {
            // Redirect to appropriate dashboard if not a student
            window.location.href = data.redirect;
        }
        // Load student data
        loadStudentData(data.user_id);
    })
    .catch(error => {
        console.error('Authentication check failed:', error);
    });
}

// Format date to remove time component
function formatDateOnly(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// Load student data
function loadStudentData(userId) {
    // Get student info
    fetch(`/student/user-info?user_id=${userId}`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('student-name').textContent = data.name;
        document.getElementById('student-usn').textContent = data.usn;
    })
    .catch(error => {
        console.error('Error loading student info:', error);
    });

    // Get leave status
    fetch(`/student/leave-status?user_id=${userId}`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('.leave-status-table tbody');
        tableBody.innerHTML = '';

        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="4" style="text-align: center;">No leave applications found</td>';
            tableBody.appendChild(row);
        } else {
            // Sort by submission date (newest first)
            data.sort((a, b) => new Date(b.Submission_Date) - new Date(a.Submission_Date));
            
            // Display only the most recent 3 leaves
            const recentLeaves = data.slice(0, 3);
            
            recentLeaves.forEach(leave => {
                const row = document.createElement('tr');
                
                // Format status with appropriate badge class
                let statusHtml;
                if (leave.Status === 'APPROVED') {
                    statusHtml = '<span class="status-badge status-approved">Approved</span>';
                } else if (leave.Status === 'REJECTED') {
                    statusHtml = '<span class="status-badge status-rejected">Rejected</span>';
                } else {
                    statusHtml = '<span class="status-badge status-pending">Pending</span>';
                }
                
                // Format dates to remove time component
                const startDate = formatDateOnly(leave.Start_Date);
                const endDate = formatDateOnly(leave.End_Date);
                
                row.innerHTML = `
                    <td>${leave.Type}</td>
                    <td>${startDate}</td>
                    <td>${endDate}</td>
                    <td>${statusHtml}</td>
                `;
                tableBody.appendChild(row);
            });
        }

        // Update upcoming leaves
        const upcomingLeavesList = document.querySelector('.upcoming-leaves');
        upcomingLeavesList.innerHTML = '';

        const approvedUpcomingLeaves = data.filter(leave => 
            leave.Status === 'APPROVED' && 
            new Date(leave.Start_Date) >= new Date()
        );

        if (approvedUpcomingLeaves.length === 0) {
            const listItem = document.createElement('li');
            listItem.textContent = 'No upcoming leaves';
            upcomingLeavesList.appendChild(listItem);
        } else {
            // Sort by start date (soonest first)
            approvedUpcomingLeaves.sort((a, b) => new Date(a.Start_Date) - new Date(b.Start_Date));
            
            approvedUpcomingLeaves.forEach(leave => {
                // Format dates to remove time component
                const startDate = formatDateOnly(leave.Start_Date);
                const endDate = formatDateOnly(leave.End_Date);
                
                const listItem = document.createElement('li');
                listItem.innerHTML = `<strong>${leave.Type}:</strong> ${startDate} to ${endDate}`;
                upcomingLeavesList.appendChild(listItem);
            });
        }
    })
    .catch(error => {
        console.error('Error loading leave status:', error);
    });

    // Get attendance data
    fetch(`/student/attendance?user_id=${userId}`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        // No longer needed since Leave Balance card was removed
    })
    .catch(error => {
        console.error('Error loading attendance data:', error);
    });
}

// Logout function
function logout() {
    fetch('/auth/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = '/auth/student-login';
    })
    .catch(error => {
        console.error('Logout failed:', error);
        window.location.href = '/auth/student-login';
    });
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});