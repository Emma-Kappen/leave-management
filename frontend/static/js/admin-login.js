document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const adminId = document.getElementById('admin_id').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('error-message');
            
            // Clear previous error
            errorMessage.style.display = 'none';
            errorMessage.textContent = '';
            
            // Send login request
            fetch('/auth/admin-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    admin_id: adminId,
                    password: password
                }),
                credentials: 'include'
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Login failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                // Redirect to admin dashboard
                window.location.href = data.redirect || '/admin/dashboard';
            })
            .catch(error => {
                // Show error message
                errorMessage.textContent = error.message;
                errorMessage.style.display = 'block';
            });
        });
    }
});