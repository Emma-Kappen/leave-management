from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..db import get_connection
from werkzeug.security import generate_password_hash
import json
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def restrict_to_admins():
    # Skip auth check for dashboard-data endpoint
    if request.endpoint == 'admin.admin_dashboard_data':
        return
        
    # For other endpoints, check if user is logged in and is admin
    user_id = request.cookies.get('user_id')
    if not user_id or not user_id.startswith('ADMIN'):
        return jsonify({'error': 'Access denied'}), 403

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    return render_template('/admin/admin_dashboard.html')

@admin_bp.route('/dashboard-data', methods=['GET'])
def admin_dashboard_data():
    try:
        # Get user_id from cookie or request
        user_id = request.cookies.get('user_id')
        if not user_id:
            # Try to get from query params
            user_id = request.args.get('user_id')
            
        if not user_id or not user_id.startswith('ADMIN'):
            return jsonify({'error': 'Unauthorized access'}), 403
            
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get admin info
        cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
        admin_info = cursor.fetchone()
        
        if not admin_info:
            # Create admin user if it doesn't exist
            cursor.execute(
                "INSERT INTO staff (ID, Name, E_Mail, Designation) VALUES (%s, %s, %s, %s)",
                (user_id, "Admin User", "admin@example.com", "Administrator")
            )
            connection.commit()
            
            # Fetch the newly created admin
            cursor.execute("SELECT * FROM staff WHERE ID = %s", (user_id,))
            admin_info = cursor.fetchone()
        
        # Ensure we have at least one department
        cursor.execute("SELECT COUNT(*) as count FROM Department")
        dept_count = cursor.fetchone()['count']
        
        if dept_count == 0:
            # Insert sample departments
            departments = [
                ("Computer Science", "FAC001"),
                ("Electrical Engineering", "FAC002"),
                ("Mechanical Engineering", "FAC003")
            ]
            for dept in departments:
                cursor.execute(
                    "INSERT INTO Department (Name, HOD) VALUES (%s, %s)",
                    dept
                )
            connection.commit()
        
        # Get department statistics
        cursor.execute("""
            SELECT d.Name AS Department, COUNT(s.USN) AS Student_Count
            FROM Department d
            LEFT JOIN Student s ON d.ID = s.Dept_ID
            GROUP BY d.Name
            ORDER BY d.Name
        """)
        departments = cursor.fetchall()
        
        # Get faculty list
        cursor.execute("""
            SELECT * FROM staff 
            WHERE Designation != 'Administrator'
            ORDER BY Name
        """)
        faculty_list = cursor.fetchall()
        
        # Get all leave requests
        cursor.execute("""
            SELECT lr.*, 
                   CASE 
                       WHEN lr.user_id LIKE 'STU%' THEN s.Name
                       ELSE st.Name
                   END as applicant_name
            FROM leave_requests lr
            LEFT JOIN student s ON lr.user_id = s.USN
            LEFT JOIN staff st ON lr.user_id = st.ID
            ORDER BY lr.created_at DESC
        """)
        all_leaves = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'admin': admin_info,
            'departments': departments,
            'faculty_list': faculty_list,
            'all_leaves': all_leaves
        }), 200
    except Exception as e:
        print(f"Error in dashboard data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@login_required
def get_all_users():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Get all students
        cursor.execute("SELECT USN as id, Name as name, E_Mail as email, 'Student' as role FROM student")
        students = cursor.fetchall()
        
        # Get all staff
        cursor.execute("SELECT ID as id, Name as name, E_Mail as email, Designation as role FROM staff")
        staff = cursor.fetchall()
        
        users = students + staff
        
        cursor.close()
        connection.close()
        
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if user is a student
        if user_id.startswith('STU'):
            cursor.execute("SELECT USN as id, Name as name, E_Mail as email, 'Student' as role FROM student WHERE USN = %s", (user_id,))
        else:
            cursor.execute("SELECT ID as id, Name as name, E_Mail as email, Designation as role FROM staff WHERE ID = %s", (user_id,))
        
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Update user based on ID pattern
        if user_id.startswith('STU'):
            cursor.execute("""
                UPDATE student 
                SET Name = %s, E_Mail = %s 
                WHERE USN = %s
            """, (data['name'], data['email'], user_id))
        else:
            cursor.execute("""
                UPDATE staff 
                SET Name = %s, E_Mail = %s 
                WHERE ID = %s
            """, (data['name'], data['email'], user_id))
        
        # Update password if provided
        if 'password' in data and data['password']:
            # Update users.json
            try:
                with open(os.path.join('backend', 'users.json'), 'r') as f:
                    users = json.load(f)
                
                users[user_id] = generate_password_hash(data['password'])
                
                with open(os.path.join('backend', 'users.json'), 'w') as f:
                    json.dump(users, f, indent=4)
            except Exception as e:
                return jsonify({'error': f"Failed to update password: {str(e)}"}), 500
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Delete user based on ID pattern
        if user_id.startswith('STU'):
            cursor.execute("DELETE FROM student WHERE USN = %s", (user_id,))
        else:
            cursor.execute("DELETE FROM staff WHERE ID = %s", (user_id,))
        
        # Remove from users.json
        try:
            with open(os.path.join('backend', 'users.json'), 'r') as f:
                users = json.load(f)
            
            if user_id in users:
                del users[user_id]
                
                with open(os.path.join('backend', 'users.json'), 'w') as f:
                    json.dump(users, f, indent=4)
        except Exception as e:
            pass  # Continue even if users.json update fails
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/students', methods=['POST'])
@login_required
def add_student():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['usn', 'name', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Insert new student
        cursor.execute("""
            INSERT INTO student (USN, Name, E_Mail)
            VALUES (%s, %s, %s)
        """, (data['usn'], data['name'], data['email']))
        
        # Add to users.json
        try:
            with open(os.path.join('backend', 'users.json'), 'r') as f:
                users = json.load(f)
            
            users[data['usn']] = generate_password_hash(data['password'])
            
            with open(os.path.join('backend', 'users.json'), 'w') as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            return jsonify({'error': f"Failed to update users.json: {str(e)}"}), 500
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/faculty', methods=['POST'])
@login_required
def add_faculty():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['id', 'name', 'email', 'password', 'designation']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f"'{field}' is required"}), 400
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Insert new faculty
        cursor.execute("""
            INSERT INTO staff (ID, Name, E_Mail, Designation)
            VALUES (%s, %s, %s, %s)
        """, (data['id'], data['name'], data['email'], data['designation']))
        
        # Add to users.json
        try:
            with open(os.path.join('backend', 'users.json'), 'r') as f:
                users = json.load(f)
            
            users[data['id']] = generate_password_hash(data['password'])
            
            with open(os.path.join('backend', 'users.json'), 'w') as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            return jsonify({'error': f"Failed to update users.json: {str(e)}"}), 500
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'Faculty added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/leaves', methods=['GET'])
@login_required
def get_all_leaves():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT lr.*, 
                   CASE 
                       WHEN lr.user_id LIKE 'STU%' THEN s.Name
                       ELSE st.Name
                   END as applicant_name
            FROM leave_requests lr
            LEFT JOIN student s ON lr.user_id = s.USN
            LEFT JOIN staff st ON lr.user_id = st.ID
            ORDER BY lr.created_at DESC
        """)
        
        leaves = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify(leaves), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@admin_bp.route('/leaves/update-status', methods=['POST'])
@login_required
def update_leave_status():
    try:
        data = request.get_json()
        
        if not data or 'leave_id' not in data or 'status' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        leave_id = data['leave_id']
        status = data['status'].lower()
        
        if status not in ['approved', 'rejected', 'pending']:
            return jsonify({'error': 'Invalid status value'}), 400
            
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE leave_requests
            SET status = %s
            WHERE id = %s
        """, (status, leave_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': f'Leave status updated to {status}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500