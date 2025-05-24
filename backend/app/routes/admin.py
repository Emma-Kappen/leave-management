from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..db import get_connection
from werkzeug.security import generate_password_hash
import json
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def restrict_to_admins():
    if current_user.user_type != 'staff' or not current_user.data.get('Designation') == 'Administrator':
        return jsonify({'error': 'Access denied'}), 403

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    return render_template('/admin/admin_dashboard.html')

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