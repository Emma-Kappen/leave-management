document.addEventListener('DOMContentLoaded', function() {
    const studentForm = document.getElementById('edit-student-form');
    
    if (studentForm) {
        studentForm.addEventListener('submit', function(event) {
            // Basic validation
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const department = document.getElementById('department').value;
            
            let isValid = true;
            let errorMessage = '';
            
            // Name validation
            if (name === '') {
                isValid = false;
                errorMessage += 'Name is required.\n';
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