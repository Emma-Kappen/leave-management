document.addEventListener('DOMContentLoaded', () => {
    const attendanceTableBody = document.querySelector('.attendance-table tbody');
    const noAttendanceMessage = document.querySelector('.no-attendance-message');

    // Function to fetch attendance data from the backend
    async function fetchAttendance() {
        try {
            const response = await fetch('/student/attendance');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching attendance data:', error);
            attendanceTableBody.innerHTML = `<tr><td colspan="5" class="error-message">Failed to load attendance data. Please try again later.</td></tr>`;
            return [];
        }
    }

    // Function to display attendance data in the table
    function displayAttendance(records) {
        if (records && records.length > 0) {
            noAttendanceMessage.style.display = 'none';
            attendanceTableBody.innerHTML = records.map(record => `
                <tr>
                    <td>${record.Subject_Code}</td>
                    <td>${record.Classes_Taken}</td>
                    <td>${record.Classes_Attended}</td>
                    <td>${record.Attendance_Percentage}%</td>
                </tr>
            `).join('');
        } else {
            attendanceTableBody.innerHTML = '';
            noAttendanceMessage.style.display = 'block';
        }
    }

    // Fetch and display attendance data when the page loads
    fetchAttendance().then(displayAttendance);
});