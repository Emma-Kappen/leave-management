document.addEventListener('DOMContentLoaded', () => {
    // Function to fetch leave status data from the backend API
    async function fetchLeaveStatus() {
        try {
            // Fetch leave status data from the backend
            const response = await fetch('/student/leave-status'); // Updated endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching leave status:', error);
            // Display an error message to the user
            const tableBody = document.querySelector('.leave-status-table tbody');
            tableBody.innerHTML = `<tr><td colspan="6" class="error-message">Failed to load leave status. Please try again later.</td></tr>`;
            return []; // Return an empty array in case of an error
        }
    }

    // Function to display leave status data in the table
    function displayLeaveStatus(leaves) {
        const tableBody = document.querySelector('.leave-status-table tbody');
        const noLeavesMessage = document.querySelector('.no-leaves-message');

        if (leaves && leaves.length > 0) {
            noLeavesMessage.style.display = 'none';
            tableBody.innerHTML = leaves.map(leave => `
                <tr>
                    <td>${leave.Type}</td>
                    <td>${leave.Start_Date}</td>
                    <td>${leave.End_Date}</td>
                    <td>${leave.Reason}</td>
                    <td><span class="status-badge status-${leave.Status.toLowerCase()}">${leave.Status}</span></td>
                </tr>
            `).join('');
        } else {
            tableBody.innerHTML = '';
            noLeavesMessage.style.display = 'block';
        }
    }

    // Fetch and display leave status when the page loads    // Fetch and display leave status when the page loads
    fetchLeaveStatus().then(displayLeaveStatus);
});