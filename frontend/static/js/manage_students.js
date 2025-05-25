// Manage Students JavaScript

// Handle edit student modal
function openEditModal(usn) {
    fetch(`/admin/student/${usn}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit-usn').value = data.USN;
            document.getElementById('edit-name').value = data.Name;
            document.getElementById('edit-email').value = data.E_Mail;
            document.getElementById('edit-dept').value = data.Dept_ID;
            
            // Show the modal
            document.getElementById('editStudentModal').style.display = 'block';
        })
        .catch(error => console.error('Error fetching student data:', error));
}

// Handle add student modal
function openAddModal() {
    // Fetch departments for dropdown
    fetch('/admin/departments/all')
        .then(response => response.json())
        .then(departments => {
            const deptSelect = document.getElementById('add-dept');
            deptSelect.innerHTML = '';
            
            departments.forEach(dept => {
                const option = document.createElement('option');
                option.value = dept.Dept_ID;
                option.textContent = dept.Dept_Name;
                deptSelect.appendChild(option);
            });
            
            // Show the modal
            document.getElementById('addStudentModal').style.display = 'block';
        })
        .catch(error => console.error('Error fetching departments:', error));
}

// Close modals when clicking outside
window.onclick = function(event) {
    const editModal = document.getElementById('editStudentModal');
    const addModal = document.getElementById('addStudentModal');
    
    if (event.target === editModal) {
        editModal.style.display = 'none';
    }
    
    if (event.target === addModal) {
        addModal.style.display = 'none';
    }
};

// Close modal when clicking the close button
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('studentSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.getElementById('studentsTable');
            const rows = table.getElementsByTagName('tr');
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const cells = row.getElementsByTagName('td');
                let found = false;
                
                for (let j = 0; j < cells.length - 1; j++) {
                    const cellText = cells[j].textContent.toLowerCase();
                    if (cellText.includes(searchTerm)) {
                        found = true;
                        break;
                    }
                }
                
                row.style.display = found ? '' : 'none';
            }
        });
    }
    
    // Set up event listeners for the modals
    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const usn = this.getAttribute('data-usn');
            openEditModal(usn);
        });
    });
    
    const addStudentBtn = document.getElementById('addStudentBtn');
    if (addStudentBtn) {
        addStudentBtn.addEventListener('click', openAddModal);
    }
    
    // Handle pagination
    const paginationButtons = document.querySelectorAll('.pagination-button');
    paginationButtons.forEach(button => {
        if (!button.classList.contains('disabled') && !button.classList.contains('active')) {
            button.addEventListener('click', function(e) {
                const page = this.getAttribute('data-page');
                if (page) {
                    window.location.href = `/admin/students?page=${page}`;
                }
            });
        }
    });
});