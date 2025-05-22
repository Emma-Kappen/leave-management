document.addEventListener('DOMContentLoaded', () => {
    const departmentListContainer = document.querySelector('.department-list');
    const noDepartmentsMessage = document.querySelector('.no-departments-message');

    // Function to fetch departments and users from the backend
    async function fetchDepartmentsAndUsers() {
        try {
            const response = await fetch('/admin/departments-users'); // Ensure this matches the backend route
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching departments and users:', error);
            departmentListContainer.innerHTML = `<div class="error-message">Failed to load departments and users. Please try again later.</div>`;
            return [];
        }
    }

    // Function to display departments and users
    function displayDepartmentsAndUsers(departments) {
        if (departments && departments.length > 0) {
            noDepartmentsMessage.style.display = 'none';
            departmentListContainer.innerHTML = departments.map(department => `
                <div class="department-card">
                    <h3 class="department-name">${department.name}</h3>
                    <ul class="user-list">
                        ${department.users.map(user => `<li>${user.name} (${user.role})</li>`).join('')}
                    </ul>
                </div>
            `).join('');
        } else {
            departmentListContainer.innerHTML = '';
            noDepartmentsMessage.style.display = 'block';
        }
    }

    // Fetch and display departments and users when the page loads
    fetchDepartmentsAndUsers().then(displayDepartmentsAndUsers);
});