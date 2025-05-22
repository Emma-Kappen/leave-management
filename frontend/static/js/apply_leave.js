document.addEventListener('DOMContentLoaded', () => {
    const applyLeaveForm = document.getElementById('apply-leave-form');
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const subjectSelect = document.getElementById('subject'); // Get the subject select element

    applyLeaveForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);
        const timeDifference = endDate.getTime() - startDate.getTime();
        const dayDifference = Math.ceil(timeDifference / (1000 * 3600 * 24)) + 1; // Include both start and end dates
        const selectedSubject = subjectSelect.value; // Get the selected subject

        // Basic client-side validation
        if (endDate < startDate) {
            alert('End date cannot be before the start date.');
            return;
        }

        if (dayDifference > 5) {
            alert('Leave application cannot exceed 5 days.');
            return;
        }

        if (!selectedSubject) {
            alert('Please select a subject.');
            return;
        }

        // Prepare the data to send to the backend
        const leaveData = {
            leave_type: document.getElementById('leaveType').value,
            reason: document.getElementById('reason').value,
            start_date: startDateInput.value,
            end_date: endDateInput.value
        };

        try {
            // Send the data to the backend
            const response = await fetch('/student/apply-leave', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(leaveData)
            });

            if (response.ok) {
                const result = await response.json();
                alert(result.message);
                window.location.href = 'leave_status.html'; // Redirect to leave status page
            } else {
                const errorData = await response.json();
                alert(`Failed to submit leave application: ${errorData.error || 'An error occurred.'}`);
            }
        } catch (error) {
            console.error('Error submitting leave application:', error);
            alert('Failed to submit leave application. Please try again.');
        }
    });
});