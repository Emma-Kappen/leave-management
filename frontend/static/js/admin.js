/**
 * Admin management pages functionality
 */

// Common search functionality for tables
function setupTableSearch(searchInputId, tableId, searchColumns) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;
    
    searchInput.addEventListener('keyup', function() {
        const searchTerm = this.value.toLowerCase();
        const table = document.getElementById(tableId);
        if (!table) return;
        
        const rows = table.getElementsByTagName('tr');
        
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            const cells = row.getElementsByTagName('td');
            if (cells.length === 0) continue;
            
            let found = false;
            
            for (let j = 0; j < searchColumns.length; j++) {
                const columnIndex = searchColumns[j];
                if (columnIndex < cells.length) {
                    const cellText = cells[columnIndex].textContent.toLowerCase();
                    if (cellText.includes(searchTerm)) {
                        found = true;
                        break;
                    }
                }
            }
            
            row.style.display = found ? '' : 'none';
        }
    });
}

// Setup modal functionality
function setupModal(modalId, openBtnId, closeBtnClass) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    
    const openBtn = document.getElementById(openBtnId);
    if (openBtn) {
        openBtn.onclick = function() {
            modal.style.display = 'block';
        };
    }
    
    const closeBtns = modal.getElementsByClassName(closeBtnClass);
    for (let i = 0; i < closeBtns.length; i++) {
        closeBtns[i].onclick = function() {
            modal.style.display = 'none';
        };
    }
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Handle leave request actions
function setupLeaveActions() {
    // Approve leave
    const approveButtons = document.querySelectorAll('.action-button.approve');
    approveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leaveId = this.getAttribute('data-id');
            if (confirm('Are you sure you want to approve this leave request?')) {
                // Submit form or make AJAX request
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/admin/approve-leave';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'leave_id';
                input.value = leaveId;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
    
    // Reject leave
    const rejectButtons = document.querySelectorAll('.action-button.reject');
    rejectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leaveId = this.getAttribute('data-id');
            if (confirm('Are you sure you want to reject this leave request?')) {
                // Submit form or make AJAX request
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = '/admin/reject-leave';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'leave_id';
                input.value = leaveId;
                
                form.appendChild(input);
                document.body.appendChild(form);
                form.submit();
            }
        });
    });
}

// Initialize pagination
function setupPagination(tableId, rowsPerPage = 10) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    
    if (totalPages <= 1) return; // No pagination needed
    
    const paginationContainer = document.querySelector('.pagination');
    if (!paginationContainer) return;
    
    // Clear existing pagination
    paginationContainer.innerHTML = '';
    
    // Add previous button
    const prevButton = document.createElement('button');
    prevButton.className = 'pagination-button';
    prevButton.textContent = 'Previous';
    prevButton.disabled = true;
    paginationContainer.appendChild(prevButton);
    
    // Add page buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = 'pagination-button';
        if (i === 1) pageButton.classList.add('active');
        pageButton.textContent = i;
        pageButton.dataset.page = i;
        paginationContainer.appendChild(pageButton);
    }
    
    // Add next button
    const nextButton = document.createElement('button');
    nextButton.className = 'pagination-button';
    nextButton.textContent = 'Next';
    paginationContainer.appendChild(nextButton);
    
    // Show first page
    showPage(1);
    
    // Add event listeners
    paginationContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('pagination-button')) {
            const pageButtons = document.querySelectorAll('.pagination-button');
            pageButtons.forEach(btn => btn.classList.remove('active'));
            
            if (e.target.textContent === 'Previous') {
                const activePage = parseInt(document.querySelector('.pagination-button.active').dataset.page);
                if (activePage > 1) {
                    const newPage = activePage - 1;
                    document.querySelector(`.pagination-button[data-page="${newPage}"]`).classList.add('active');
                    showPage(newPage);
                    
                    // Update button states
                    prevButton.disabled = newPage === 1;
                    nextButton.disabled = false;
                }
            } else if (e.target.textContent === 'Next') {
                const activePage = parseInt(document.querySelector('.pagination-button.active').dataset.page);
                if (activePage < totalPages) {
                    const newPage = activePage + 1;
                    document.querySelector(`.pagination-button[data-page="${newPage}"]`).classList.add('active');
                    showPage(newPage);
                    
                    // Update button states
                    prevButton.disabled = false;
                    nextButton.disabled = newPage === totalPages;
                }
            } else {
                e.target.classList.add('active');
                const page = parseInt(e.target.dataset.page);
                showPage(page);
                
                // Update button states
                prevButton.disabled = page === 1;
                nextButton.disabled = page === totalPages;
            }
        }
    });
    
    // Function to show a specific page
    function showPage(page) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        
        rows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? '' : 'none';
        });
    }
}

// Initialize charts for reports page
function initReportsCharts() {
    const monthlyChartCanvas = document.getElementById('monthlyChart');
    if (!monthlyChartCanvas) return;
    
    // Monthly chart data would be populated from the server
    // This is just a placeholder
    const monthlyData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [
            {
                label: 'Student Leaves',
                data: [12, 19, 3, 5, 2, 3, 7, 8, 9, 10, 11, 4],
                backgroundColor: 'rgba(59, 130, 246, 0.5)',
                borderColor: 'rgb(59, 130, 246)',
                borderWidth: 1
            },
            {
                label: 'Faculty Leaves',
                data: [7, 11, 5, 8, 3, 7, 9, 5, 7, 4, 6, 8],
                backgroundColor: 'rgba(16, 185, 129, 0.5)',
                borderColor: 'rgb(16, 185, 129)',
                borderWidth: 1
            }
        ]
    };
    
    // Create monthly chart
    if (typeof Chart !== 'undefined') {
        new Chart(monthlyChartCanvas, {
            type: 'bar',
            data: monthlyData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Setup search for different tables
    setupTableSearch('studentSearch', 'studentsTable', [0, 1, 2, 3, 4]);
    setupTableSearch('facultySearch', 'facultyTable', [0, 1, 2, 3]);
    setupTableSearch('departmentSearch', 'departmentsTable', [0, 1]);
    setupTableSearch('subjectSearch', 'subjectsTable', [0, 1, 2, 3]);
    setupTableSearch('leaveSearch', 'leavesTable', [0, 1]);
    
    // Setup modals
    setupModal('addDepartmentModal', 'addDepartmentBtn', 'close');
    setupModal('editDepartmentModal', null, 'close');
    setupModal('addSubjectModal', 'addSubjectBtn', 'close');
    setupModal('editSubjectModal', null, 'close');
    setupModal('viewLeaveModal', null, 'close');
    
    // Setup leave actions
    setupLeaveActions();
    
    // Setup pagination for tables
    setupPagination('studentsTable');
    setupPagination('facultyTable');
    setupPagination('subjectsTable');
    setupPagination('leavesTable');
    
    // Initialize charts for reports page
    initReportsCharts();
});

// Export functionality for reports
function exportReport() {
    alert('Exporting report as CSV...');
    // In a real implementation, this would generate and download a CSV file
}

// Filter functionality for reports
function filterReportData() {
    const year = document.getElementById('yearFilter')?.value;
    const department = document.getElementById('departmentFilter')?.value;
    
    // In a real implementation, this would fetch filtered data from the server
    // and update the charts and tables
    console.log(`Filtering data for year: ${year}, department: ${department || 'All'}`);
}