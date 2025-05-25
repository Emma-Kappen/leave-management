document.addEventListener('DOMContentLoaded', function() {
    const studentForm = document.getElementById('add-student-form');
    
    if (studentForm) {
        studentForm.addEventListener('submit', function(event) {
            // Basic validation
            const usn = document.getElementById('usn').value.trim();
            const email = document.getElementById('email').value.trim();
            const department = document.getElementById('department').value;
            
            let isValid = true;
            let errorMessage = '';
            
            // USN validation (example pattern: 1RV20CS001)
            if (!/^\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}$/.test(usn)) {
                isValid = false;
                errorMessage += 'USN format is invalid. It should follow the pattern like 1RV20CS001.\n';
            }
            
            // Email validation
            if (!email.includes('@')) {
                isValid = false;
                errorMessage += 'Please enter a valid email address.\n';
            }
            
            // Department selection validation
            if (!department) {
                isValid = false;
                errorMessage += 'Please select a department.\n';
            }
            
            if (!isValid) {
                event.preventDefault();
                alert('Please fix the following errors:\n' + errorMessage);
            }
        });
    }
});