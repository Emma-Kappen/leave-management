document.addEventListener('DOMContentLoaded', () => {
    const leaveRequestsTableBody = document.querySelector('.leave-requests-table tbody');
    const noRequestsMessage = document.querySelector('.no-requests-message');

    // Function to fetch leave requests from the backend
    async function fetchLeaveRequests() {
        try {
            const response = await fetch('/faculty/leave-requests'); // Updated endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching leave requests:', error);
            leaveRequestsTableBody.innerHTML = `<tr><td colspan="8" class="error-message">Failed to load leave requests. Please try again later.</td></tr>`;
            return [];
        }
    }

    // Function to display leave requests in the table
    function displayLeaveRequests(requests) {
        if (requests && requests.length > 0) {
            noRequestsMessage.style.display = 'none';
            leaveRequestsTableBody.innerHTML = requests.map(request => `
                <tr>
                    <td>${request.student_name}</td>
                    <td>${request.leave_type}</td>
                    <td>${request.subject}</td>
                    <td>${request.start_date}</td>
                    <td>${request.end_date}</td>
                    <td>${request.reason}</td>
                    <td><span class="status-badge status-${request.status.toLowerCase()}">${request.status}</span></td>
                    <td class="action-buttons">
                        <button class="action-button approve-button" data-leave-id="${request.leave_id}">Approve</button>
                        <button class="action-button reject-button" data-leave-id="${request.leave_id}">Reject</button>
                    </td>
                </tr>
            `).join('');

            // Add event listeners to the approve and reject buttons after they are added to the DOM
            addActionEventListeners();

        } else {
            leaveRequestsTableBody.innerHTML = '';
            noRequestsMessage.style.display = 'block';
        }
    }

    // Function to handle approve/reject actions
    function addActionEventListeners() {
        const approveButtons = document.querySelectorAll('.approve-button');
        const rejectButtons = document.querySelectorAll('.reject-button');

        approveButtons.forEach(button => {
            button.addEventListener('click', async (event) => {
                const leaveId = event.target.dataset.leaveId;
                await updateLeaveStatus(leaveId, 'approved');
            });
        });

        rejectButtons.forEach(button => {
            button.addEventListener('click', async (event) => {
                const leaveId = event.target.dataset.leaveId;
                await updateLeaveStatus(leaveId, 'rejected');
            });
        });
    }

    // Function to send the approve/reject action to the backend
    async function updateLeaveStatus(leaveId, status) {
        try {
            const response = await fetch(`/faculty/leave-requests/${leaveId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: status.toUpperCase() }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // After successful update, refresh the leave requests list
            fetchLeaveRequests().then(displayLeaveRequests);
        } catch (error) {
            console.error(`Error updating leave status to ${status} for leave ID ${leaveId}:`, error);
            alert(`Failed to ${status} leave request. Please try again.`);
        }
    }

    // Fetch and display leave requests when the page loads
    fetchLeaveRequests().then(displayLeaveRequests);
});