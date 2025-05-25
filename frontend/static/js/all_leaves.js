// All Leaves JavaScript

// Load all leaves when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadAllLeaves();
});

// Function to load all leave requests
function loadAllLeaves() {
    fetch('/admin/get-all-leaves', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to load leave requests');
        }
        return response.json();
    })
    .then(leaves => {
        displayLeaves(leaves);
    })
    .catch(error => {
        console.error('Error loading leave requests:', error);
        document.querySelector('.no-leaves-message').style.display = 'block';
    });
}

// Function to display leaves in the table
function displayLeaves(leaves) {
    const tableBody = document.querySelector('.all-leaves-table tbody');
    tableBody.innerHTML = '';
    
    if (leaves.length === 0) {
        document.querySelector('.no-leaves-message').style.display = 'block';
        return;
    }
    
    leaves.forEach(leave => {
        const row = document.createElement('tr');
        
        // Format dates
        const startDate = new Date(leave.Start_Date).toLocaleDateString();
        const endDate = new Date(leave.End_Date).toLocaleDateString();
        const submissionDate = new Date(leave.Submission_Date).toLocaleDateString();
        
        // Create status badge
        let statusBadge;
        if (leave.Approval_Status === 'APPROVED') {
            statusBadge = '<span class="status-badge status-approved">Approved</span>';
        } else if (leave.Approval_Status === 'REJECTED') {
            statusBadge = '<span class="status-badge status-rejected">Rejected</span>';
        } else {
            statusBadge = '<span class="status-badge status-pending">Pending</span>';
        }
        
        row.innerHTML = `
            <td>Student</td>
            <td>${leave.Student_Name}</td>
            <td>${leave.Leave_Type}</td>
            <td>${leave.Subject_Title || 'N/A'}</td>
            <td>${startDate}</td>
            <td>${endDate}</td>
            <td>${leave.Reason}</td>
            <td>${statusBadge}</td>
            <td>${submissionDate}</td>
        `;
        tableBody.appendChild(row);
    });
}