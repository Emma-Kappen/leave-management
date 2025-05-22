document.addEventListener('DOMContentLoaded', () => {
    const leaveHistoryTableBody = document.querySelector('.leave-history-table tbody');
    const noHistoryMessage = document.querySelector('.no-history-message');

    // Function to fetch faculty leave history from the backend
    async function fetchLeaveHistory() {
        try {
            const response = await fetch('/faculty/leave-history'); // Updated endpoint
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching leave history:', error);
            leaveHistoryTableBody.innerHTML = `<tr><td colspan="8" class="error-message">Failed to load leave history. Please try again later.</td></tr>`;
            return [];
        }
    }

    // Function to display leave history in the table
    function displayLeaveHistory(history) {
        if (history && history.length > 0) {
            noHistoryMessage.style.display = 'none';
            leaveHistoryTableBody.innerHTML = history.map(record => `
                <tr>
                    <td>${record.student_name}</td>
                    <td>${record.leave_type}</td>
                    <td>${record.subject}</td>
                    <td>${record.start_date}</td>
                    <td>${record.end_date}</td>
                    <td>${record.reason}</td>
                    <td><span class="status-badge status-${record.status.toLowerCase()}">${record.status}</span></td>
                    <td>${record.action_taken_on}</td>
                </tr>
            `).join('');
        } else {
            leaveHistoryTableBody.innerHTML = '';
            noHistoryMessage.style.display = 'block';
        }
    }

    // Fetch and display leave history when the page loads
    fetchLeaveHistory().then(displayLeaveHistory);
});