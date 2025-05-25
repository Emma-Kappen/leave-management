// Faculty Dashboard JavaScript

// Check if user is authenticated
function checkAuth() {
    fetch('/auth/check-auth', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            // Redirect to login page if not authenticated
            window.location.href = '/auth/faculty-login';
            throw new Error('Not authenticated');
        }
        return response.json();
    })
    .then(data => {
        if (data.role !== 'faculty') {
            // Redirect to appropriate dashboard if not a faculty
            window.location.href = data.redirect;
        }
        // Load faculty data
        loadFacultyData(data.user_id);
    })
    .catch(error => {
        console.error('Authentication check failed:', error);
    });
}

// Load faculty data
function loadFacultyData(userId) {
    fetch(`/faculty/user-info?user_id=${userId}`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('faculty-name').textContent = data.name;
        document.getElementById('faculty-id').textContent = data.id;
    })
    .catch(error => {
        console.error('Error loading faculty info:', error);
    });

    // Load pending leave requests
    loadPendingLeaveRequests();
}

// Load pending leave requests
function loadPendingLeaveRequests() {
    fetch('/faculty/pending-leaves', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('.leave-requests-table tbody');
        tableBody.innerHTML = '';

        if (data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="6" style="text-align: center;">No pending leave requests</td>';
            tableBody.appendChild(row);
        } else {
            data.forEach(request => {
                const row = document.createElement('tr');
                
                // Format dates
                const startDate = new Date(request.Start_Date).toISOString().split('T')[0];
                const endDate = new Date(request.End_Date).toISOString().split('T')[0];
                const dateRange = startDate === endDate ? startDate : `${startDate} to ${endDate}`;
                
                row.innerHTML = `
                    <td>${request.Student_Name}</td>
                    <td>${request.Subject_Title}</td>
                    <td>${request.Leave_Type}</td>
                    <td>${dateRange}</td>
                    <td><span class="status-badge status-pending">Pending</span></td>
                    <td>
                        <button onclick="approveLeave(${request.Leave_ID})" class="approve-btn">Approve</button>
                        <button onclick="rejectLeave(${request.Leave_ID})" class="reject-btn">Reject</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        }
    })
    .catch(error => {
        console.error('Error loading pending leave requests:', error);
        const tableBody = document.querySelector('.leave-requests-table tbody');
        tableBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Error loading leave requests</td></tr>';
    });
}

// Approve leave request
function approveLeave(leaveId) {
    updateLeaveStatus(leaveId, 'APPROVED');
}

// Reject leave request
function rejectLeave(leaveId) {
    updateLeaveStatus(leaveId, 'REJECTED');
}

// Update leave status
function updateLeaveStatus(leaveId, status) {
    fetch('/faculty/update-leave-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            leave_id: leaveId,
            status: status
        }),
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update leave status');
        }
        return response.json();
    })
    .then(data => {
        // Reload pending leave requests
        loadPendingLeaveRequests();
    })
    .catch(error => {
        console.error('Error updating leave status:', error);
        alert('Failed to update leave status. Please try again.');
    });
}

// Logout function
function handleLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    logoutBtn.textContent = 'Logging out...';
    logoutBtn.disabled = true;
    
    fetch('/auth/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = '/auth/faculty-login';
    })
    .catch(error => {
        console.error('Logout failed:', error);
        window.location.href = '/auth/faculty-login';
    });
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});