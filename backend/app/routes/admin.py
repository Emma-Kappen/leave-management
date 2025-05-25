from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from ..db import execute_query
from ..models import Staff, Student

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    return render_template('admin/admin_dashboard.html')

@admin_bp.route('/manage-users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    return render_template('admin/manage_users.html')

@admin_bp.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    
    if request.method == 'GET':
        return render_template('admin/add_user.html')
    
    # Handle POST request to add a new user
    data = request.form or request.get_json()
    
    try:
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        department = data.get('department')
        
        if role == 'student':
            # Generate a new USN
            query = "SELECT MAX(CAST(SUBSTRING(USN, 2) AS UNSIGNED)) as max_id FROM Student"
            result = execute_query(query)
            next_id = 1
            if result and result[0]['max_id']:
                next_id = int(result[0]['max_id']) + 1
            
            usn = f"S{next_id:04d}"
            
            # Get department ID
            dept_id = None
            if department:
                query = "SELECT ID FROM Department WHERE Name = %s"
                result = execute_query(query, (department,))
                if result:
                    dept_id = result[0]['ID']
            
            # Insert new student
            query = """
            INSERT INTO Student (USN, Name, E_Mail, Dept_ID, Password)
            VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(query, (usn, name, email, dept_id, password), fetch=False)
            
            return jsonify({'success': True, 'message': f'Student added successfully with USN: {usn}'})
            
        elif role in ['faculty', 'admin']:
            # Generate a new Faculty ID
            query = "SELECT MAX(CAST(SUBSTRING(ID, 2) AS UNSIGNED)) as max_id FROM Staff"
            result = execute_query(query)
            next_id = 1
            if result and result[0]['max_id']:
                next_id = int(result[0]['max_id']) + 1
            
            staff_id = f"F{next_id:03d}"
            designation = 'Administrator' if role == 'admin' else 'Professor'
            
            # Insert new staff
            query = """
            INSERT INTO Staff (ID, Name, E_Mail, Designation, Password)
            VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(query, (staff_id, name, email, designation, password), fetch=False)
            
            return jsonify({'success': True, 'message': f'Staff added successfully with ID: {staff_id}'})
        
        return jsonify({'error': 'Invalid role specified'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/edit-user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    
    if request.method == 'GET':
        user_data = None
        
        # Check if it's a student
        if user_id.startswith('S'):
            query = "SELECT * FROM Student WHERE USN = %s"
            result = execute_query(query, (user_id,))
            if result:
                user_data = {
                    'id': result[0]['USN'],
                    'name': result[0]['Name'],
                    'email': result[0]['E_Mail'],
                    'role': 'student',
                    'dept_id': result[0]['Dept_ID']
                }
                
                # Get department name
                if user_data['dept_id']:
                    query = "SELECT Name FROM Department WHERE ID = %s"
                    dept_result = execute_query(query, (user_data['dept_id'],))
                    if dept_result:
                        user_data['department'] = dept_result[0]['Name']
        
        # Check if it's a staff member
        elif user_id.startswith(('F', 'FAC')):
            query = "SELECT * FROM Staff WHERE ID = %s"
            result = execute_query(query, (user_id,))
            if result:
                user_data = {
                    'id': result[0]['ID'],
                    'name': result[0]['Name'],
                    'email': result[0]['E_Mail'],
                    'role': 'admin' if result[0]['Designation'] == 'Administrator' else 'faculty'
                }
        
        if not user_data:
            return render_template('error/404.html', message="User not found"), 404
            
        return render_template('admin/edit_user.html', user=user_data)
    
    # Handle POST request to update user
    data = request.form or request.get_json()
    
    try:
        name = data.get('name')
        email = data.get('email')
        role = data.get('role')
        department = data.get('department')
        
        # Update student
        if user_id.startswith('S'):
            dept_id = None
            if department:
                query = "SELECT ID FROM Department WHERE Name = %s"
                result = execute_query(query, (department,))
                if result:
                    dept_id = result[0]['ID']
            
            query = """
            UPDATE Student 
            SET Name = %s, E_Mail = %s, Dept_ID = %s
            WHERE USN = %s
            """
            execute_query(query, (name, email, dept_id, user_id), fetch=False)
            
        # Update staff
        elif user_id.startswith(('F', 'FAC')):
            designation = 'Administrator' if role == 'admin' else 'Professor'
            
            query = """
            UPDATE Staff 
            SET Name = %s, E_Mail = %s, Designation = %s
            WHERE ID = %s
            """
            execute_query(query, (name, email, designation, user_id), fetch=False)
        
        return jsonify({'success': True, 'message': 'User updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/delete-user/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    
    try:
        # Delete student
        if user_id.startswith('S'):
            query = "DELETE FROM Student WHERE USN = %s"
            execute_query(query, (user_id,), fetch=False)
            
        # Delete staff
        elif user_id.startswith(('F', 'FAC')):
            query = "DELETE FROM Staff WHERE ID = %s"
            execute_query(query, (user_id,), fetch=False)
        
        return jsonify({'success': True, 'message': 'User deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/get-users')
@login_required
def get_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get all students
        students_query = """
        SELECT s.USN, s.Name, s.E_Mail, d.Name as Department
        FROM Student s
        LEFT JOIN Department d ON s.Dept_ID = d.ID
        """
        students = execute_query(students_query)
        
        # Get all staff
        staff_query = """
        SELECT ID, Name, E_Mail, Designation
        FROM Staff
        """
        staff = execute_query(staff_query)
        
        # Format the results
        users = []
        
        for student in students:
            users.append({
                'id': student['USN'],
                'name': student['Name'],
                'email': student['E_Mail'],
                'role': 'Student',
                'department': student['Department'] or 'N/A'
            })
            
        for staff_member in staff:
            users.append({
                'id': staff_member['ID'],
                'name': staff_member['Name'],
                'email': staff_member['E_Mail'],
                'role': 'Admin' if staff_member['Designation'] == 'Administrator' else 'Faculty',
                'department': 'N/A'
            })
            
        return jsonify(users)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/all-leaves')
@login_required
def all_leaves():
    if current_user.role != 'admin':
        return redirect(url_for(f'{current_user.role}.dashboard'))
    
    return render_template('admin/all_leaves.html')

@admin_bp.route('/get-all-leaves')
@login_required
def get_all_leaves():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Get all student leaves with details
        query = """
        SELECT l.Leave_ID, l.Applicant_ID, s.Name as Student_Name, 
               l.Leave_Type, l.Start_Date, l.End_Date, l.Reason, 
               l.Submission_Date, l.Approval_Status,
               sub.Code as Subject_Code, sub.Title as Subject_Title,
               d.Name as Department_Name
        FROM `Leave` l
        JOIN Student s ON l.Applicant_ID = s.USN
        LEFT JOIN Teaches t ON s.USN = t.USN
        LEFT JOIN Subject sub ON t.Subject_Code = sub.Code
        LEFT JOIN Department d ON s.Dept_ID = d.ID
        ORDER BY l.Submission_Date DESC
        """
        
        leaves = execute_query(query)
        return jsonify(leaves)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500