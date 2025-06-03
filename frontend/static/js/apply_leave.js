// Apply Leave JavaScript

// Check if user is authenticated
function checkAuth() {
    fetch('/auth/check-auth', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            // Redirect to login page if not authenticated
            window.location.href = '/auth/student-login';
            throw new Error('Not authenticated');
        }
        return response.json();
    })
    .then(data => {
        if (data.role !== 'student') {
            // Redirect to appropriate dashboard if not a student
            window.location.href = data.redirect;
        }
        // Load student's subjects
        loadSubjects();
    })
    .catch(error => {
        console.error('Authentication check failed:', error);
    });
}

// Load subjects for the student
function loadSubjects() {
    fetch('/student/subjects', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(subjects => {
        const subjectDropdown = document.getElementById('subject');
        
        // Clear existing options except the first one
        while (subjectDropdown.options.length > 1) {
            subjectDropdown.remove(1);
        }
        
        if (subjects.length === 0) {
            const option = document.createElement('option');
            option.text = 'No subjects available';
            option.disabled = true;
            subjectDropdown.add(option);
        } else {
            // Add each subject to the dropdown
            subjects.forEach(subject => {
                const option = document.createElement('option');
                option.value = subject.Code;
                option.text = subject.Title;
                subjectDropdown.add(option);
            });
        }
    })
    .catch(error => {
        console.error('Error loading subjects:', error);
    });
}

// Validate form before submission
function validateForm() {
    const startDate = new Date(document.getElementById('startDate').value);
    const endDate = new Date(document.getElementById('endDate').value);
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time part for proper comparison
    
    if (startDate < today) {
        alert('Start date cannot be in the past');
        return false;
    }
    
    if (endDate < startDate) {
        alert('End date cannot be before start date');
        return false;
    }
    
    return true;
}

// Handle form submission
function handleSubmit(event) {
    event.preventDefault();
    
    if (!validateForm()) {
        return;
    }
    
    const form = document.getElementById('apply-leave-form');
    const formData = new FormData(form);
    
    // Convert FormData to JSON for the main form data
    const jsonData = {};
    formData.forEach((value, key) => {
        if (key !== 'attachment') { // Skip file input for JSON
            jsonData[key] = value;
        }
    });
    
    // Check if there's a file to upload
    const fileInput = document.getElementById('attachment');
    const hasFile = fileInput.files && fileInput.files.length > 0;
    
    // Submit the form data
    if (hasFile) {
        // If there's a file, use FormData approach
        submitWithFile(formData);
    } else {
        // If no file, use JSON approach
        submitWithoutFile(jsonData);
    }
}

// Submit form with file attachment
function submitWithFile(formData) {
    fetch('/student/apply-leave-with-file', {
        method: 'POST',
        body: formData,
        credentials: 'include'
    })
    .then(handleResponse)
    .then(handleSuccess)
    .catch(handleError);
}

// Submit form without file attachment
function submitWithoutFile(jsonData) {
    fetch('/student/apply-leave', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData),
        credentials: 'include'
    })
    .then(handleResponse)
    .then(handleSuccess)
    .catch(handleError);
}

// Handle the response from the server
function handleResponse(response) {
    if (!response.ok) {
        // Check if the response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to submit leave application');
            });
        } else {
            throw new Error('Server error: Failed to submit leave application');
        }
    }
    
    // Check if the response is JSON before parsing
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
        return response.json();
    } else {
        return { message: 'Leave application submitted successfully!' };
    }
}

// Handle successful submission
function handleSuccess(data) {
    alert(data.message || 'Leave application submitted successfully!');
    window.location.href = '/student/dashboard';
}

// Handle submission error
function handleError(error) {
    alert(error.message || 'An error occurred while submitting your application.');
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    // Set up form submission handler
    const form = document.getElementById('apply-leave-form');
    form.addEventListener('submit', handleSubmit);
    
    // Set minimum date for date inputs to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('startDate').min = today;
    document.getElementById('endDate').min = today;
});