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
            window.location.href = '/'; // Redirect to login page
        } else {
            alert('Failed to log out. Please try again.');
        }
    } catch (error) {
        console.error('Error during logout:', error);
        alert('An error occurred while logging out.');
    }
}

// Fetch faculty information
async function fetchFacultyInfo() {
    try {
        const response = await fetch('/admin/users/FAC001');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const facultyInfo = await response.json();
        console.log('Faculty Info:', facultyInfo);
        
        // Display faculty information
        document.getElementById('faculty-name').textContent = facultyInfo.name || 'Unknown';
        document.getElementById('faculty-email').textContent = facultyInfo.email || 'No email available';
        document.getElementById('faculty-designation').textContent = facultyInfo.role || 'Faculty';
    } catch (error) {
        console.error('Error fetching faculty info:', error);
        document.getElementById('faculty-info').innerHTML = '<p>Could not load faculty information.</p>';
    }
}

// Fetch students
async function fetchStudents() {
    try {
        const response = await fetch('/admin/users');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json();
        const students = users.filter(user => user.id.startsWith('1CS') || user.id.startsWith('STU'));
        
        console.log('Students:', students);
        
        // Display students
        const studentsList = document.getElementById('students-list');
        if (students.length === 0) {
            studentsList.innerHTML = '<p>No students found.</p>';
            return;
        }
        
        let html = '<table class="table"><thead><tr><th>ID</th><th>Name</th><th>Email</th></tr></thead><tbody>';
        students.forEach(student => {
            html += `<tr>
                <td>${student.id}</td>
                <td>${student.name}</td>
                <td>${student.email}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        studentsList.innerHTML = html;
    } catch (error) {
        console.error('Error fetching students:', error);
        document.getElementById('students-list').innerHTML = '<p>Could not load students data.</p>';
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
        
        // Display leave requests
        const leaveRequestsList = document.getElementById('leave-requests-list');
        if (leaveRequests.length === 0) {
            leaveRequestsList.innerHTML = '<p>No pending leave requests.</p>';
            return;
        }
        
        let html = '<table class="table"><thead><tr><th>Student</th><th>Type</th><th>From</th><th>To</th><th>Reason</th><th>Actions</th></tr></thead><tbody>';
        leaveRequests.forEach(request => {
            html += `<tr>
                <td>${request.applicant_name || request.user_id}</td>
                <td>${request.leave_type || 'N/A'}</td>
                <td>${new Date(request.start_date).toLocaleDateString()}</td>
                <td>${new Date(request.end_date).toLocaleDateString()}</td>
                <td>${request.reason}</td>
                <td>
                    <button class="btn btn-success btn-sm" onclick="approveLeave(${request.id})">Approve</button>
                    <button class="btn btn-danger btn-sm" onclick="rejectLeave(${request.id})">Reject</button>
                </td>
            </tr>`;
        });
        html += '</tbody></table>';
        leaveRequestsList.innerHTML = html;
    } catch (error) {
        console.error('Error fetching leave requests:', error);
        document.getElementById('leave-requests-list').innerHTML = '<p>Could not load leave requests.</p>';
    }
}

// Approve leave request
async function approveLeave(leaveId) {
    try {
        const response = await fetch(`/faculty/leave-requests/${leaveId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: 'approved' })
        });
        
        if (response.ok) {
            alert('Leave request approved successfully!');
            fetchPendingLeaveRequests(); // Refresh the list
        } else {
            const error = await response.json();
            alert(`Failed to approve leave: ${error.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error approving leave:', error);
        alert('An error occurred while approving the leave request.');
    }
}

// Reject leave request
async function rejectLeave(leaveId) {
    try {
        const response = await fetch(`/faculty/leave-requests/${leaveId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: 'rejected' })
        });
        
        if (response.ok) {
            alert('Leave request rejected successfully!');
            fetchPendingLeaveRequests(); // Refresh the list
        } else {
            const error = await response.json();
            alert(`Failed to reject leave: ${error.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error rejecting leave:', error);
        alert('An error occurred while rejecting the leave request.');
    }
}

// Call the functions when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchFacultyInfo();
    fetchStudents();
    fetchPendingLeaveRequests();
});