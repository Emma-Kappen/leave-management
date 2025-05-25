document.addEventListener('DOMContentLoaded', function() {
    // Get user ID from cookie
    const userId = getCookie('user_id');
    
    if (userId) {
        // Fetch leave status
        fetchLeaveStatus(userId);
    } else {
        // Redirect to login if no user ID is found
        window.location.href = '/';
    }
});

// Function to get cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fetch leave status
function fetchLeaveStatus(userId) {
    fetch(`/student/leave-status?user_id=${userId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch leave status');
            }
            return response.json();
        })
        .then(data => {
            // Update leave status table
            updateLeaveStatusTable(data);
        })
        .catch(error => {
            console.error('Error fetching leave status:', error);
            showErrorMessage('Failed to load leave applications. Please try again later.');
        });
}

// Update leave status table
function updateLeaveStatusTable(leaves) {
    const tableBody = document.getElementById('leave-status-body');
    const noLeavesMessage = document.querySelector('.no-leaves-message');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    if (leaves && leaves.length > 0) {
        // Hide no leaves message
        noLeavesMessage.style.display = 'none';
        
        // Add new rows
        leaves.forEach(leave => {
            const row = document.createElement('tr');
            
            // Determine status class
            let statusClass = '';
            switch(leave.Status) {
                case 'PENDING':
                    statusClass = 'status-pending';
                    break;
                case 'APPROVED':
                    statusClass = 'status-approved';
                    break;
                case 'REJECTED':
                    statusClass = 'status-rejected';
                    break;
            }
            
            row.innerHTML = `
                <td>${leave.Type}</td>
                <td>${leave.Subject || 'N/A'}</td>
                <td>${formatDate(leave.Start_Date)}</td>
                <td>${formatDate(leave.End_Date)}</td>
                <td>${leave.Reason}</td>
                <td><span class="status-badge ${statusClass}">${leave.Status}</span></td>
            `;
            tableBody.appendChild(row);
        });
    } else {
        // Show no leaves message
        noLeavesMessage.style.display = 'block';
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center;">No leave applications found.</td>
            </tr>
        `;
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toISOString().split('T')[0];
}

// Show error message
function showErrorMessage(message) {
    const container = document.querySelector('.leave-status-container');
    const errorDiv = document.createElement('div');
    errorDiv.style.backgroundColor = '#fee2e2';
    errorDiv.style.color = '#991b1b';
    errorDiv.style.padding = '1rem';
    errorDiv.style.borderRadius = '0.375rem';
    errorDiv.style.marginBottom = '1rem';
    errorDiv.textContent = message;
    
    // Insert at the top of the container
    container.insertBefore(errorDiv, container.firstChild);
}