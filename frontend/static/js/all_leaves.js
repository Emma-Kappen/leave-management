document.addEventListener('DOMContentLoaded', () => {
    const allLeavesTableBody = document.querySelector('.all-leaves-table tbody');
    const noLeavesMessage = document.querySelector('.no-leaves-message');

    // Function to fetch all leave requests from the backend
    async function fetchAllLeaves() {
        try {
            // Ensure the URL matches the backend route
            const response = await fetch('/admin/leaves');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching all leave requests:', error);
            allLeavesTableBody.innerHTML = `<tr><td colspan="9" class="error-message">Failed to load leave requests. Please try again later.</td></tr>`;
            return [];
        }
    }

    // Function to display all leave requests in the table
    function displayAllLeaves(leaves) {
        if (leaves && leaves.length > 0) {
            noLeavesMessage.style.display = 'none';
            allLeavesTableBody.innerHTML = leaves.map(leave => `
                <tr>
                    <td>${leave.user_type}</td>
                    <td>${leave.name}</td>
                    <td>${leave.leave_type}</td>
                    <td>${leave.subject || '-'}</td>
                    <td>${leave.start_date}</td>
                    <td>${leave.end_date}</td>
                    <td>${leave.reason}</td>
                    <td><span class="status-badge status-${leave.status.toLowerCase()}">${leave.status}</span></td>
                    <td>${leave.submitted_on}</td>
                </tr>
            `).join('');
        } else {
            allLeavesTableBody.innerHTML = '';
            noLeavesMessage.style.display = 'block';
        }
    }

    // Fetch and display all leave requests when the page loads
    fetchAllLeaves().then(displayAllLeaves);
});